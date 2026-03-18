import pygame

from game.active_abilities import get_ability_definition
from game.input.menu_actions import MenuActions
from game.render.characters import ANIM_IDLE, CharacterSpriteLibrary
from game.ui.widgets import (
    build_centered_menu_rects,
    draw_centered_text,
    hovered_index,
    wrap_text,
)


class LobbyScreen:
    def __init__(self) -> None:
        self.selected_index = 0
        self.hover_index: int | None = None
        self.hover_variant_index: int | None = None
        self.character_library = CharacterSpriteLibrary()
        self._character_preview_cache: dict[tuple[str, int], pygame.Surface | None] = {}

    def handle_input(
        self,
        actions: MenuActions,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        *,
        selected_character_name: str,
        selected_character_id: str,
        selected_map_name: str,
        selected_ability_id: str,
        selected_ability_name: str,
        selected_variant_id: str,
        selected_variant_name: str,
    ) -> str | None:
        _, panel_start_y, row_height = self._layout_metrics(surface)
        option_labels = self._option_labels(
            selected_map_name,
            selected_ability_name,
            selected_variant_name,
        )
        option_rects = build_centered_menu_rects(
            surface=surface,
            font=body_font,
            options=option_labels,
            start_y=panel_start_y,
            row_height=row_height,
            min_width=self._row_min_width(surface),
        )
        variant_rects = self._variant_node_rects(option_rects[3])
        hovered_variant_index = hovered_index(actions.mouse_position, variant_rects)

        hovered = hovered_index(actions.mouse_position, option_rects)
        self.hover_index = hovered
        self.hover_variant_index = hovered_variant_index
        if actions.mouse_moved and hovered is not None:
            self.selected_index = hovered
        if actions.mouse_moved and hovered_variant_index is not None:
            self.selected_index = 3

        if actions.navigate_up:
            self.selected_index = (self.selected_index - 1) % len(option_labels)
        if actions.navigate_down:
            self.selected_index = (self.selected_index + 1) % len(option_labels)

        if actions.navigate_left:
            return self._command_for_navigation(self.selected_index, step=-1)
        if actions.navigate_right:
            return self._command_for_navigation(self.selected_index, step=1)

        if actions.mouse_left_click and hovered_variant_index is not None:
            self.selected_index = 3
            ability = get_ability_definition(selected_ability_id)
            if ability is None or hovered_variant_index >= len(ability.variants):
                return None
            return f"variant_set:{ability.variants[hovered_variant_index].variant_id}"
        if actions.mouse_left_click and hovered is not None:
            self.selected_index = hovered
            return self._command_for_select(self.selected_index)

        if actions.select:
            return self._command_for_select(self.selected_index)
        if actions.back:
            return "back_main_menu"
        return None

    def render(
        self,
        surface: pygame.Surface,
        title_font: pygame.font.Font,
        body_font: pygame.font.Font,
        *,
        selected_character_name: str,
        selected_character_id: str,
        selected_map_name: str,
        selected_ability_id: str,
        selected_ability_name: str,
        selected_variant_id: str,
        selected_variant_name: str,
        character_count: int,
        map_count: int,
        ability_count: int,
        small_font: pygame.font.Font,
    ) -> None:
        title_y, panel_start_y, row_height = self._layout_metrics(surface)
        option_labels = self._option_labels(
            selected_map_name,
            selected_ability_name,
            selected_variant_name,
        )
        option_rects = build_centered_menu_rects(
            surface=surface,
            font=body_font,
            options=option_labels,
            start_y=panel_start_y,
            row_height=row_height,
            min_width=self._row_min_width(surface),
        )
        variant_rects = self._variant_node_rects(option_rects[3])
        ability_panel_rect = self._ability_panel_rect(option_rects[4], variant_rects)
        selected_ability = get_ability_definition(selected_ability_id)

        draw_centered_text(surface, title_font, "Lobby", title_y, (245, 245, 245))
        draw_centered_text(
            surface,
            body_font,
            f"Characters: {character_count}  |  Maps: {map_count}  |  Abilities: {ability_count}",
            title_y + max(30, row_height - 6),
            (188, 188, 188),
        )
        draw_centered_text(
            surface,
            body_font,
            "Use Left/Right to change selections.",
            title_y + max(56, row_height + 18),
            (168, 168, 168),
        )

        for index, option in enumerate(option_labels):
            if index == 3:
                continue
            rect = option_rects[index]
            is_selected = index == self.selected_index
            is_hovered = index == self.hover_index
            self._draw_option_button(
                surface=surface,
                font=body_font,
                rect=rect,
                label=option,
                selected=is_selected,
                hovered=is_hovered,
            )

            if index == 0:
                preview = self._character_preview(
                    selected_character_id,
                    max_height=max(28, rect.height - 16),
                )
                if preview is not None:
                    preview_rect = preview.get_rect(center=rect.center)
                    surface.blit(preview, preview_rect)
                else:
                    label = body_font.render(selected_character_name, True, (225, 225, 225))
                    surface.blit(label, label.get_rect(center=rect.center))

        self._draw_ability_module(
            surface=surface,
            body_font=body_font,
            small_font=small_font,
            panel_rect=ability_panel_rect,
            ability_rect=option_rects[2],
            ability_label=option_labels[2],
            variant_rects=variant_rects,
            selected_ability=selected_ability,
            selected_variant_id=selected_variant_id,
        )

    @staticmethod
    def _option_labels(
        selected_map_name: str,
        selected_ability_name: str,
        selected_variant_name: str,
    ) -> list[str]:
        return [
            "Character",
            f"Map: {selected_map_name}",
            f"Ability: {selected_ability_name}",
            f"Variant: {selected_variant_name}",
            "Start Run",
            "Back to Main Menu",
        ]

    @staticmethod
    def _ability_panel_rect(
        reference_rect: pygame.Rect,
        variant_rects: list[pygame.Rect],
    ) -> pygame.Rect:
        if not variant_rects:
            return pygame.Rect(0, 0, 0, 0)

        padding_y = 10
        left = reference_rect.left
        right = reference_rect.right
        top = min(rect.top for rect in variant_rects) - padding_y
        bottom = max(rect.bottom for rect in variant_rects) + padding_y
        return pygame.Rect(left, top, right - left, bottom - top)

    @staticmethod
    def _row_min_width(surface: pygame.Surface) -> int:
        return max(280, min(560, surface.get_width() - 72))

    @staticmethod
    def _variant_node_rects(row_rect: pygame.Rect) -> list[pygame.Rect]:
        gap = 8
        node_width = max(80, min(160, (row_rect.width // 3) - 20))
        node_height = max(28, row_rect.height - 12)
        top = row_rect.y + ((row_rect.height - node_height) // 2)
        total_width = (node_width * 3) + (gap * 2)
        rects: list[pygame.Rect] = []
        left = row_rect.centerx - (total_width // 2)
        for index in range(3):
            rects.append(
                pygame.Rect(
                    left + index * (node_width + gap),
                    top,
                    node_width,
                    node_height,
                )
            )
        return rects

    def _draw_ability_module(
        self,
        *,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
        panel_rect: pygame.Rect,
        ability_rect: pygame.Rect,
        ability_label: str,
        variant_rects: list[pygame.Rect],
        selected_ability,
        selected_variant_id: str,
    ) -> None:
        pygame.draw.rect(surface, (24, 28, 34), panel_rect, border_radius=10)
        pygame.draw.rect(surface, (88, 96, 108), panel_rect, width=2, border_radius=10)

        self._draw_option_button(
            surface=surface,
            font=body_font,
            rect=ability_rect,
            label=ability_label,
            selected=self.selected_index == 2,
            hovered=self.hover_index == 2,
        )

        variant_descriptions = ["Variant", "Variant", "Variant"]
        variant_ids = ["", "", ""]
        if selected_ability is not None:
            variant_descriptions = [
                self._format_variant_description(variant.description)
                for variant in selected_ability.variants[:3]
            ]
            variant_ids = [variant.variant_id for variant in selected_ability.variants[:3]]

        for index, rect in enumerate(variant_rects):
            is_selected = selected_variant_id == variant_ids[index]
            is_hovered = self.hover_variant_index == index
            if is_selected:
                background = (64, 72, 86)
                border = (255, 235, 120)
                text_color = (255, 235, 120)
            elif is_hovered:
                background = (52, 58, 70)
                border = (140, 150, 165)
                text_color = (225, 225, 225)
            else:
                background = (34, 38, 46)
                border = (88, 96, 108)
                text_color = (205, 205, 205)

            pygame.draw.rect(surface, background, rect, border_radius=8)
            pygame.draw.rect(surface, border, rect, width=2, border_radius=8)

            lines = self._wrap_font_lines(
                small_font,
                variant_descriptions[index],
                max_width=rect.width - 18,
                max_lines=2,
            )
            self._draw_fitted_variant_text(
                surface=surface,
                font=small_font,
                rect=rect,
                lines=lines,
                color=text_color,
            )

    @staticmethod
    def _wrap_font_lines(
        font: pygame.font.Font,
        text: str,
        *,
        max_width: int,
        max_lines: int,
    ) -> list[str]:
        lines = wrap_text(font, text, max_width=max_width)
        if len(lines) <= max_lines:
            return lines
        return lines[:max_lines]

    @staticmethod
    def _format_variant_description(text: str) -> str:
        return text.rstrip().rstrip(".")

    @staticmethod
    def _draw_fitted_variant_text(
        *,
        surface: pygame.Surface,
        font: pygame.font.Font,
        rect: pygame.Rect,
        lines: list[str],
        color: tuple[int, int, int],
    ) -> None:
        if not lines:
            return

        rendered_lines = [font.render(line, True, color) for line in lines]
        max_width = rect.width - 18
        max_height = rect.height - 12
        width_scale = min(
            1.0,
            min(
                max_width / max(1, rendered.get_width())
                for rendered in rendered_lines
            ),
        )
        total_height = sum(rendered.get_height() for rendered in rendered_lines)
        gap = 2
        total_height += gap * max(0, len(rendered_lines) - 1)
        height_scale = min(1.0, max_height / max(1, total_height))
        final_scale = min(0.86, width_scale, height_scale)

        if final_scale < 1.0:
            rendered_lines = [
                pygame.transform.scale(
                    rendered,
                    (
                        max(1, int(round(rendered.get_width() * final_scale))),
                        max(1, int(round(rendered.get_height() * final_scale))),
                    ),
                )
                for rendered in rendered_lines
            ]

        scaled_total_height = sum(rendered.get_height() for rendered in rendered_lines)
        scaled_total_height += gap * max(0, len(rendered_lines) - 1)
        start_y = rect.centery - (scaled_total_height // 2)
        current_y = start_y
        for rendered in rendered_lines:
            rendered_rect = rendered.get_rect(centerx=rect.centerx, y=current_y)
            surface.blit(rendered, rendered_rect)
            current_y += rendered.get_height() + gap

    def _character_preview(self, character_id: str, max_height: int) -> pygame.Surface | None:
        cache_key = (character_id, max_height)
        if cache_key in self._character_preview_cache:
            return self._character_preview_cache[cache_key]

        clip = self.character_library.get_animation_clip(character_id, ANIM_IDLE)
        if clip is None or not clip.frames:
            self._character_preview_cache[cache_key] = None
            return None

        frame = clip.frames[0]
        width, height = frame.get_size()
        if height <= 0:
            self._character_preview_cache[cache_key] = None
            return None

        scale = max(0.1, min(2.5, float(max_height) / float(height)))
        if scale <= 0.0:
            self._character_preview_cache[cache_key] = None
            return None

        scaled = pygame.transform.scale(
            frame,
            (
                max(1, int(round(width * scale))),
                max(1, int(round(height * scale))),
            ),
        )
        self._character_preview_cache[cache_key] = scaled
        return scaled

    @staticmethod
    def _draw_option_button(
        *,
        surface: pygame.Surface,
        font: pygame.font.Font,
        rect: pygame.Rect,
        label: str,
        selected: bool,
        hovered: bool,
    ) -> None:
        if selected:
            background = (64, 72, 86)
            border = (255, 235, 120)
            text_color = (255, 235, 120)
        elif hovered:
            background = (52, 58, 70)
            border = (140, 150, 165)
            text_color = (255, 235, 120)
        else:
            background = (34, 38, 46)
            border = (88, 96, 108)
            text_color = (210, 210, 210)

        pygame.draw.rect(surface, background, rect, border_radius=8)
        pygame.draw.rect(surface, border, rect, width=2, border_radius=8)

        rendered = font.render(label, True, text_color)
        rendered_rect = rendered.get_rect(midleft=(rect.left + 18, rect.centery))
        surface.blit(rendered, rendered_rect)

    def _layout_metrics(self, surface: pygame.Surface) -> tuple[int, int, int]:
        height = surface.get_height()
        top_padding = max(16, height // 20)
        title_y = top_padding + max(26, height // 11)
        panel_top = title_y + max(96, height // 5)
        bottom_padding = max(20, height // 14)
        available_height = max(120, height - panel_top - bottom_padding)
        row_height = max(
            34,
            min(
                72,
                available_height
                // max(
                    1,
                    len(self._option_labels("", "", "")),
                ),
            ),
        )
        panel_start_y = panel_top + (row_height // 2)
        return title_y, panel_start_y, row_height

    @staticmethod
    def _command_for_navigation(index: int, *, step: int) -> str | None:
        if index == 0:
            return "character_prev" if step < 0 else "character_next"
        if index == 1:
            return "map_prev" if step < 0 else "map_next"
        if index == 2:
            return "ability_prev" if step < 0 else "ability_next"
        if index == 3:
            return "variant_prev" if step < 0 else "variant_next"
        return None

    @staticmethod
    def _command_for_select(index: int) -> str | None:
        if index == 0:
            return "character_next"
        if index == 1:
            return "map_next"
        if index == 2:
            return "ability_next"
        if index == 3:
            return "variant_next"
        if index == 4:
            return "start_run"
        if index == 5:
            return "back_main_menu"
        return None
