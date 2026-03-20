from __future__ import annotations

from pathlib import Path

import pygame

from game.active_abilities import resolve_ability_selection
from game.core.enhancements import (
    EnhancementDefinition,
    EnhancementIconRole,
    EnhancementOffer,
    enhancement_pool_label,
    get_enhancement,
)
from game.input.menu_actions import MenuActions
from game.render.effects import EffectClipLibrary
from game.render.fonts import UIFonts
from game.render.spritesheet import load_pixelart_image
from game.ui.widgets import draw_centered_text, hovered_index, wrap_text

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ROCK_ICON_PATH = PROJECT_ROOT / "assets" / "effects" / "Rock.png"
UTILITY_ICON_PATH = PROJECT_ROOT / "assets" / "upgrades" / "utility.png"


class EnhancementChoiceScreen:
    def __init__(self) -> None:
        self.selected_index = 0
        self.hover_index: int | None = None
        self._last_offer_signature: tuple[str, str, str] | None = None
        self._effect_library = EffectClipLibrary()
        self._base_rock_icon = load_pixelart_image(ROCK_ICON_PATH, scale_multiple=1)
        self._base_utility_icon = load_pixelart_image(UTILITY_ICON_PATH, scale_multiple=1)
        self._ability_icon_cache: dict[str, pygame.Surface | None] = {}

    def handle_input(
        self,
        actions: MenuActions,
        surface: pygame.Surface,
        offer: EnhancementOffer,
    ) -> int | None:
        self._sync_offer(offer)
        rects = self._card_rects(surface)
        self.hover_index = hovered_index(actions.mouse_position, rects)

        if actions.mouse_moved and self.hover_index is not None:
            self.selected_index = self.hover_index

        if actions.navigate_left:
            self.selected_index = max(0, self.selected_index - 1)
        if actions.navigate_right:
            self.selected_index = min(2, self.selected_index + 1)

        if actions.mouse_left_click and self.hover_index is not None:
            self.selected_index = self.hover_index
            return self.selected_index
        if actions.select:
            return self.selected_index
        return None

    def render(
        self,
        surface: pygame.Surface,
        fonts: UIFonts,
        offer: EnhancementOffer,
        *,
        active_ability_id: str,
    ) -> None:
        self._sync_offer(offer)
        title_y = max(92, surface.get_height() // 7)
        draw_centered_text(surface, fonts.title, "Choose an Enhancement", title_y, (248, 248, 250))
        draw_centered_text(
            surface,
            fonts.small,
            f"Difficulty {offer.trigger_difficulty_factor:.1f}",
            title_y + 42,
            (205, 210, 218),
        )

        rects = self._card_rects(surface)
        option_ids = offer.option_ids
        for index, rect in enumerate(rects):
            definition = get_enhancement(option_ids[index])
            if definition is None:
                continue
            self._draw_card(
                surface,
                rect,
                fonts,
                definition,
                active_ability_id=active_ability_id,
                is_selected=index == self.selected_index,
                is_hovered=index == self.hover_index,
            )

        draw_centered_text(
            surface,
            fonts.small,
            "Use Left and Right, then confirm your choice.",
            rects[0].bottom + 30,
            (214, 218, 225),
        )

    def _draw_card(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        fonts: UIFonts,
        definition: EnhancementDefinition,
        *,
        active_ability_id: str,
        is_selected: bool,
        is_hovered: bool,
    ) -> None:
        if is_selected:
            background = (70, 78, 94)
            border = (255, 228, 110)
            text_color = (255, 246, 215)
        elif is_hovered:
            background = (56, 62, 76)
            border = (146, 156, 174)
            text_color = (240, 242, 248)
        else:
            background = (34, 38, 46)
            border = (92, 100, 114)
            text_color = (232, 234, 240)

        pygame.draw.rect(surface, background, rect, border_radius=12)
        pygame.draw.rect(surface, border, rect, width=2, border_radius=12)

        pool_label = fonts.small.render(
            enhancement_pool_label(definition.pool),
            True,
            (194, 200, 208),
        )
        surface.blit(pool_label, pool_label.get_rect(midtop=(rect.centerx, rect.top + 12)))

        icon_rect = pygame.Rect(0, 0, 68, 68)
        icon_rect.midtop = (rect.centerx, rect.top + 42)
        self._draw_icon(surface, icon_rect, definition, active_ability_id)

        name = fonts.heading.render(definition.display_name, True, text_color)
        surface.blit(name, name.get_rect(midtop=(rect.centerx, icon_rect.bottom + 14)))

        description_font = fonts.body
        wrapped_lines = wrap_text(description_font, definition.description, rect.width - 32)
        line_y = icon_rect.bottom + 68
        for line in wrapped_lines[:3]:
            rendered = description_font.render(line, True, (228, 230, 236))
            surface.blit(rendered, rendered.get_rect(center=(rect.centerx, line_y)))
            line_y += rendered.get_height() + 6

    def _draw_icon(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        definition: EnhancementDefinition,
        active_ability_id: str,
    ) -> None:
        pygame.draw.rect(surface, (22, 26, 32), rect, border_radius=10)
        pygame.draw.rect(surface, (108, 116, 132), rect, width=2, border_radius=10)

        icon = self._resolve_icon(definition, active_ability_id)
        if icon is None:
            return

        inner_rect = rect.inflate(-10, -10)
        scaled = pygame.transform.scale(icon, inner_rect.size)
        surface.blit(scaled, scaled.get_rect(center=inner_rect.center))

    def _resolve_icon(
        self,
        definition: EnhancementDefinition,
        active_ability_id: str,
    ) -> pygame.Surface | None:
        if definition.icon_role is EnhancementIconRole.ROCK:
            return self._base_rock_icon
        if definition.icon_role is EnhancementIconRole.UTILITY:
            return self._base_utility_icon
        return self._ability_icon(active_ability_id)

    def _ability_icon(self, ability_id: str) -> pygame.Surface | None:
        if ability_id in self._ability_icon_cache:
            return self._ability_icon_cache[ability_id]

        ability, _ = resolve_ability_selection(ability_id, "")
        if ability.logbook_preview_icon_path:
            icon_path = (PROJECT_ROOT / ability.logbook_preview_icon_path).resolve()
            icon = load_pixelart_image(icon_path, scale_multiple=1)
            self._ability_icon_cache[ability_id] = icon
            return icon
        if ability.logbook_preview_effect_id:
            clip = self._effect_library.get_clip(ability.logbook_preview_effect_id)
            if clip is not None and clip.frames:
                frame = (
                    clip.frames[-1]
                    if ability.logbook_preview_frame == "last"
                    else clip.frames[0]
                )
                self._ability_icon_cache[ability_id] = frame
                return frame

        self._ability_icon_cache[ability_id] = None
        return None

    def _sync_offer(self, offer: EnhancementOffer) -> None:
        signature = tuple(offer.option_ids)
        if signature != self._last_offer_signature:
            self._last_offer_signature = signature
            self.selected_index = 0
            self.hover_index = None

    @staticmethod
    def _card_rects(surface: pygame.Surface) -> list[pygame.Rect]:
        screen_width, screen_height = surface.get_size()
        gap = 20
        width = min(280, max(220, (screen_width - 120 - gap * 2) // 3))
        height = min(310, max(248, screen_height // 2))
        total_width = (width * 3) + (gap * 2)
        start_x = (screen_width - total_width) // 2
        top = max(150, (screen_height - height) // 2)
        return [
            pygame.Rect(start_x + index * (width + gap), top, width, height)
            for index in range(3)
        ]
