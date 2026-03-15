from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame

from game.active_abilities import ActiveAbilityDefinition, list_active_abilities
from game.core.blessings import BlessingDefinition, list_blessings
from game.core.enemies import EnemyProfile, EnemyTier
from game.core.enemy_catalog import list_enemy_profiles
from game.core.profile import PlayerProfile
from game.input.menu_actions import MenuActions
from game.render.blessings import BlessingSpriteLibrary
from game.render.effects import EffectClipLibrary
from game.render.enemies import EnemySpriteLibrary
from game.render.spritesheet import load_pixelart_image, pixelart_upscale_surface
from game.ui.widgets import draw_centered_text, hovered_index, wrap_text

TAB_ENEMIES = "enemies"
TAB_BLESSINGS = "blessings"
TAB_ABILITIES = "abilities"
PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True, slots=True)
class TabDefinition:
    tab_id: str
    label: str


@dataclass(slots=True)
class TimedEffectAnimationState:
    frame_index: int = 0
    frame_progress_seconds: float = 0.0


class LogbookScreen:
    def __init__(self) -> None:
        self.tabs = [
            TabDefinition(TAB_ENEMIES, "Enemies"),
            TabDefinition(TAB_BLESSINGS, "Blessings"),
            TabDefinition(TAB_ABILITIES, "Abilities"),
        ]
        self.selected_tab_index = 0
        self.focus_area = "grid"
        self.detail_entry_id: str | None = None
        self.grid_selection_by_tab: dict[str, int] = {
            TAB_ENEMIES: 0,
            TAB_BLESSINGS: 0,
            TAB_ABILITIES: 0,
        }
        self.hover_tab_index: int | None = None
        self.hover_grid_index: int | None = None
        self.hover_back = False
        self.hover_prev_entry = False
        self.hover_next_entry = False
        self.enemy_library = EnemySpriteLibrary()
        self.blessing_library = BlessingSpriteLibrary(world_icon_scale=4)
        self.effect_library = EffectClipLibrary()
        self.enemy_profiles = list_enemy_profiles()
        self.blessings = list_blessings()
        self.active_abilities = list_active_abilities()
        self._enemy_preview_cache: dict[str, pygame.Surface | None] = {}
        self._ability_preview_cache: dict[str, pygame.Surface | None] = {}
        self._ability_effect_animation_states: dict[
            tuple[str, str, str], TimedEffectAnimationState
        ] = {}
        self._last_render_time_seconds: float | None = None

    def selection_signature(self) -> tuple[str, int, int | None, str | None]:
        active_tab = self._active_tab_id()
        return (
            self.focus_area,
            self.selected_tab_index,
            self.grid_selection_by_tab.get(active_tab),
            self.detail_entry_id,
        )

    def handle_input(
        self,
        actions: MenuActions,
        surface: pygame.Surface,
        profile: PlayerProfile,
    ) -> str | None:
        active_tab = self._active_tab_id()
        encountered_enemy_ids = profile.logbook.encountered_enemy_ids
        encountered_blessing_ids = profile.logbook.encountered_blessing_ids

        tab_rects = self._tab_rects(surface)
        back_rect = self._back_rect(surface)
        if self.detail_entry_id is None:
            entries = self._entries_for_tab(active_tab)
            grid_rects = self._grid_rects(surface, len(entries))
            self.hover_tab_index = hovered_index(actions.mouse_position, tab_rects)
            self.hover_grid_index = hovered_index(actions.mouse_position, grid_rects)
            self.hover_back = back_rect.collidepoint(actions.mouse_position or (-1, -1))

            if actions.mouse_moved:
                if self.hover_grid_index is not None:
                    self.grid_selection_by_tab[active_tab] = self.hover_grid_index
                    self.focus_area = "grid"
                elif self.hover_back:
                    self.focus_area = "back"
                elif self.hover_tab_index is not None:
                    self.focus_area = "tabs"

            if actions.mouse_left_click:
                if self.hover_tab_index is not None:
                    self.selected_tab_index = self.hover_tab_index
                    self.focus_area = "tabs"
                    return None
                if self.hover_grid_index is not None:
                    self.grid_selection_by_tab[active_tab] = self.hover_grid_index
                    self.focus_area = "grid"
                    return self._open_detail_if_unlocked(
                        tab_id=active_tab,
                        index=self.hover_grid_index,
                        encountered_enemy_ids=encountered_enemy_ids,
                        encountered_blessing_ids=encountered_blessing_ids,
                    )
                if self.hover_back:
                    self.focus_area = "back"
                    return "back"

            if self.focus_area == "tabs":
                if actions.navigate_left:
                    self.selected_tab_index = (self.selected_tab_index - 1) % len(self.tabs)
                if actions.navigate_right:
                    self.selected_tab_index = (self.selected_tab_index + 1) % len(self.tabs)
                if actions.navigate_down:
                    self.focus_area = "grid"
                if actions.select:
                    return None
            elif self.focus_area == "grid":
                self._handle_grid_navigation(actions, surface, active_tab)
                if actions.select:
                    return self._open_detail_if_unlocked(
                        tab_id=active_tab,
                        index=self.grid_selection_by_tab[active_tab],
                        encountered_enemy_ids=encountered_enemy_ids,
                        encountered_blessing_ids=encountered_blessing_ids,
                    )
            elif self.focus_area == "back":
                if actions.navigate_up:
                    self.focus_area = "grid"
                if actions.select:
                    return "back"

            if actions.back:
                return "back"
            return None

        self.hover_tab_index = None
        self.hover_grid_index = None
        prev_rect = self._detail_prev_rect(surface)
        next_rect = self._detail_next_rect(surface)
        self.hover_back = back_rect.collidepoint(actions.mouse_position or (-1, -1))
        self.hover_prev_entry = prev_rect.collidepoint(actions.mouse_position or (-1, -1))
        self.hover_next_entry = next_rect.collidepoint(actions.mouse_position or (-1, -1))
        if actions.mouse_moved:
            if self.hover_prev_entry:
                self.focus_area = "detail_prev"
            elif self.hover_next_entry:
                self.focus_area = "detail_next"
            elif self.hover_back:
                self.focus_area = "back"
        if actions.mouse_left_click and self.hover_prev_entry:
            self._cycle_detail_entry(profile, step=-1)
            return None
        if actions.mouse_left_click and self.hover_next_entry:
            self._cycle_detail_entry(profile, step=1)
            return None
        if actions.mouse_left_click and self.hover_back:
            self.detail_entry_id = None
            return None
        if actions.navigate_left:
            self._cycle_detail_entry(profile, step=-1)
            return None
        if actions.navigate_right:
            self._cycle_detail_entry(profile, step=1)
            return None
        if actions.select and self.focus_area == "detail_prev":
            self._cycle_detail_entry(profile, step=-1)
            return None
        if actions.select and self.focus_area == "detail_next":
            self._cycle_detail_entry(profile, step=1)
            return None
        if actions.select or actions.back:
            self.detail_entry_id = None
        return None

    def render(
        self,
        surface: pygame.Surface,
        profile: PlayerProfile,
        title_font: pygame.font.Font,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
    ) -> None:
        render_now_seconds = pygame.time.get_ticks() / 1000.0
        if self._last_render_time_seconds is None:
            render_dt = 0.0
        else:
            render_dt = max(0.0, min(0.1, render_now_seconds - self._last_render_time_seconds))
        self._last_render_time_seconds = render_now_seconds

        width, _ = surface.get_size()
        draw_centered_text(surface, title_font, "Logbook", 60, (245, 245, 245))
        draw_centered_text(
            surface,
            body_font,
            "Enemies, blessings, and active abilities",
            102,
            (180, 180, 180),
        )

        active_tab = self._active_tab_id()
        self._draw_tabs(surface, body_font)

        if self.detail_entry_id is None:
            self._ability_effect_animation_states.clear()
            if active_tab == TAB_ENEMIES:
                self._draw_enemy_overview(surface, profile, body_font, small_font)
            elif active_tab == TAB_BLESSINGS:
                self._draw_blessing_overview(surface, profile, body_font, small_font)
            else:
                self._draw_ability_overview(surface, body_font, small_font)
        elif active_tab == TAB_ENEMIES:
            self._draw_enemy_detail(surface, profile, body_font, small_font, render_dt)
        elif active_tab == TAB_BLESSINGS:
            self._ability_effect_animation_states.clear()
            self._draw_blessing_detail(surface, profile, body_font, small_font)
        else:
            self._ability_effect_animation_states.clear()
            self._draw_ability_detail(surface, profile, body_font, small_font)

        back_rect = self._back_rect(surface)
        back_label = "Back to Overview" if self.detail_entry_id is not None else "Back"
        self._draw_button(
            surface,
            small_font if self.detail_entry_id is not None else body_font,
            back_rect,
            back_label,
            selected=self.focus_area == "back",
            hovered=self.hover_back,
        )
        if self.detail_entry_id is None:
            if active_tab == TAB_ENEMIES:
                discovered = len(profile.logbook.encountered_enemy_ids)
                total = len(self.enemy_profiles)
                progress_text = f"Discovered: {discovered} / {total}"
            elif active_tab == TAB_BLESSINGS:
                discovered = len(profile.logbook.encountered_blessing_ids)
                total = len(self.blessings)
                progress_text = f"Discovered: {discovered} / {total}"
            else:
                total = len(self.active_abilities)
                progress_text = f"Entries: {total} / {total}"
            rendered = small_font.render(progress_text, True, (175, 175, 175))
            surface.blit(rendered, (width - rendered.get_width() - 36, 112))

    def _draw_tabs(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        for index, tab in enumerate(self.tabs):
            rect = self._tab_rects(surface)[index]
            self._draw_button(
                surface,
                font,
                rect,
                tab.label,
                selected=self.selected_tab_index == index and self.focus_area == "tabs",
                hovered=self.hover_tab_index == index or self.selected_tab_index == index,
            )

    def _draw_enemy_overview(
        self,
        surface: pygame.Surface,
        profile: PlayerProfile,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
    ) -> None:
        rects = self._grid_rects(surface, len(self.enemy_profiles))
        selected_index = self.grid_selection_by_tab[TAB_ENEMIES]
        for index, enemy_profile in enumerate(self.enemy_profiles):
            encountered = enemy_profile.profile_id in profile.logbook.encountered_enemy_ids
            self._draw_grid_entry(
                surface,
                body_font,
                small_font,
                rects[index],
                title=enemy_profile.display_name if encountered else "Unknown",
                subtitle="",
                sprite=self._enemy_preview(enemy_profile.profile_id) if encountered else None,
                selected=self.focus_area == "grid" and selected_index == index,
                hovered=self.hover_grid_index == index,
                unlocked=encountered,
                accent_color=(self._enemy_tier_color(enemy_profile.tier) if encountered else None),
            )

    def _draw_blessing_overview(
        self,
        surface: pygame.Surface,
        profile: PlayerProfile,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
    ) -> None:
        rects = self._grid_rects(surface, len(self.blessings))
        selected_index = self.grid_selection_by_tab[TAB_BLESSINGS]
        for index, blessing in enumerate(self.blessings):
            encountered = blessing.blessing_id in profile.logbook.encountered_blessing_ids
            self._draw_grid_entry(
                surface,
                body_font,
                small_font,
                rects[index],
                title=blessing.display_name if encountered else "Unknown",
                subtitle="",
                sprite=self.blessing_library.get_icon(blessing.blessing_id, scale_multiple=4)
                if encountered
                else None,
                selected=self.focus_area == "grid" and selected_index == index,
                hovered=self.hover_grid_index == index,
                unlocked=encountered,
            )

    def _draw_ability_overview(
        self,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
    ) -> None:
        rects = self._grid_rects(surface, len(self.active_abilities))
        selected_index = self.grid_selection_by_tab[TAB_ABILITIES]
        for index, ability in enumerate(self.active_abilities):
            self._draw_grid_entry(
                surface,
                body_font,
                small_font,
                rects[index],
                title=ability.display_name,
                subtitle="",
                sprite=self._ability_preview(ability, target_size=56),
                selected=self.focus_area == "grid" and selected_index == index,
                hovered=self.hover_grid_index == index,
                unlocked=True,
                accent_color=None,
            )

    def _draw_enemy_detail(
        self,
        surface: pygame.Surface,
        profile: PlayerProfile,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
        render_dt: float,
    ) -> None:
        if self.detail_entry_id is None:
            return
        enemy = next(
            (entry for entry in self.enemy_profiles if entry.profile_id == self.detail_entry_id),
            None,
        )
        if enemy is None or enemy.profile_id not in profile.logbook.encountered_enemy_ids:
            self.detail_entry_id = None
            return

        self._draw_enemy_detail_panel(
            surface=surface,
            body_font=body_font,
            small_font=small_font,
            enemy=enemy,
            render_dt=render_dt,
        )
        self._draw_detail_nav(surface, body_font, profile)

    def _draw_enemy_detail_panel(
        self,
        *,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
        enemy: EnemyProfile,
        render_dt: float,
    ) -> None:
        panel_rect = self._detail_panel_rect(surface)
        pygame.draw.rect(surface, (30, 34, 42), panel_rect, border_radius=12)
        pygame.draw.rect(surface, (108, 116, 128), panel_rect, width=2, border_radius=12)

        title_render = body_font.render(enemy.display_name, True, (235, 235, 235))
        surface.blit(title_render, (panel_rect.x + 28, panel_rect.y + 24))

        sprite = self._enemy_preview(enemy.profile_id)
        if sprite is not None:
            sprite_rect = sprite.get_rect(center=(panel_rect.x + 116, panel_rect.y + 118))
            surface.blit(sprite, sprite_rect)

        left_x = panel_rect.x + 28
        stats_y = panel_rect.y + 190
        stats_title = small_font.render("Stats", True, (180, 180, 180))
        surface.blit(stats_title, (left_x, stats_y))
        stat_lines = [
            f"Tier: {enemy.tier.value.title()}",
            f"Tags: {', '.join(enemy.tags) if enemy.tags else 'None'}",
            f"Max HP: {enemy.stats.max_health}",
            f"Speed: {enemy.stats.speed:.0f}",
            f"Touch Damage: {enemy.stats.touch_damage}",
            f"Coin Drop: {enemy.stats.coin_drop_value}",
        ]
        for index, line in enumerate(stat_lines):
            rendered = body_font.render(line, True, (225, 225, 225))
            surface.blit(rendered, (left_x, stats_y + 30 + (index * 30)))

        right_x = panel_rect.x + max(240, panel_rect.width // 2)
        detail_width = panel_rect.right - right_x - 16
        detail_title_render = small_font.render("Abilities", True, (180, 180, 180))
        surface.blit(detail_title_render, (right_x, panel_rect.y + 78))

        content_y = panel_rect.y + 108
        content_bottom = panel_rect.bottom - 16
        active_effect_keys: set[tuple[str, str, str]] = set()

        if not enemy.abilities:
            empty = body_font.render("No special abilities recorded.", True, (220, 220, 220))
            surface.blit(empty, (right_x, content_y))
            self._ability_effect_animation_states.clear()
            return

        for ability in enemy.abilities:
            if content_y + body_font.get_linesize() > content_bottom:
                break

            ability_name = body_font.render(ability.display_name, True, (225, 225, 225))
            surface.blit(ability_name, (right_x, content_y))
            content_y += 24

            description_lines = wrap_text(
                body_font,
                ability.description or "No description recorded.",
                max_width=max(120, detail_width),
            )
            for line in description_lines:
                if content_y + body_font.get_linesize() > content_bottom:
                    break
                rendered = body_font.render(line, True, (220, 220, 220))
                surface.blit(rendered, (right_x, content_y))
                content_y += 24

            effect_ids = [
                effect_id
                for effect_id in (
                    ability.loop_effect_id,
                    ability.fire_effect_id,
                    ability.projectile_effect_id,
                )
                if effect_id
            ]
            deduped_effect_ids = list(dict.fromkeys(effect_ids))

            for effect_id in deduped_effect_ids:
                clip = self.effect_library.get_clip(effect_id)
                if clip is None or not clip.frames:
                    continue
                key = (enemy.profile_id, ability.ability_id, effect_id)
                active_effect_keys.add(key)
                state = self._ability_effect_animation_states.setdefault(
                    key,
                    TimedEffectAnimationState(),
                )
                self._advance_looping_animation(
                    state,
                    fps=float(clip.fps),
                    frame_count=len(clip.frames),
                    render_dt=render_dt,
                )
                frame = clip.frames[state.frame_index]
                frame_rect = frame.get_rect(topleft=(right_x, content_y + 4))
                if frame_rect.bottom > content_bottom:
                    break
                surface.blit(frame, frame_rect)
                content_y = frame_rect.bottom + 10

            content_y += 8

        self._ability_effect_animation_states = {
            key: state
            for key, state in self._ability_effect_animation_states.items()
            if key in active_effect_keys
        }

    def _draw_blessing_detail(
        self,
        surface: pygame.Surface,
        profile: PlayerProfile,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
    ) -> None:
        if self.detail_entry_id is None:
            return
        blessing = next(
            (entry for entry in self.blessings if entry.blessing_id == self.detail_entry_id),
            None,
        )
        if blessing is None or blessing.blessing_id not in profile.logbook.encountered_blessing_ids:
            self.detail_entry_id = None
            return

        detail_lines = wrap_text(body_font, blessing.description, max_width=430)
        self._draw_detail_panel(
            surface=surface,
            body_font=body_font,
            small_font=small_font,
            title=blessing.display_name,
            sprite=self.blessing_library.get_icon(blessing.blessing_id, scale_multiple=5),
            stat_lines=[
                "Type: Blessing",
                "Status: Discovered",
            ],
            detail_lines=detail_lines,
            detail_title="Effect",
        )
        self._draw_detail_nav(surface, body_font, profile)

    def _draw_ability_detail(
        self,
        surface: pygame.Surface,
        profile: PlayerProfile,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
    ) -> None:
        if self.detail_entry_id is None:
            return

        ability = next(
            (entry for entry in self.active_abilities if entry.ability_id == self.detail_entry_id),
            None,
        )
        if ability is None:
            self.detail_entry_id = None
            return

        panel_rect = self._detail_panel_rect(surface)
        pygame.draw.rect(surface, (30, 34, 42), panel_rect, border_radius=12)
        pygame.draw.rect(surface, (108, 116, 128), panel_rect, width=2, border_radius=12)

        title_render = body_font.render(ability.display_name, True, (235, 235, 235))
        surface.blit(title_render, (panel_rect.x + 28, panel_rect.y + 24))

        description_lines = wrap_text(
            body_font,
            ability.description,
            max_width=panel_rect.width - 56,
        )
        for index, line in enumerate(description_lines[:2]):
            rendered = body_font.render(line, True, (220, 220, 220))
            surface.blit(rendered, (panel_rect.x + 28, panel_rect.y + 58 + (index * 24)))

        preview = self._ability_preview(ability, target_size=108)
        if preview is not None:
            preview_rect = preview.get_rect(topright=(panel_rect.right - 24, panel_rect.y + 26))
            surface.blit(preview, preview_rect)

        variants_title = small_font.render("Variants", True, (180, 180, 180))
        surface.blit(variants_title, (panel_rect.x + 28, panel_rect.y + 122))

        content_width = panel_rect.width - 56
        gap = 14
        card_width = (content_width - (gap * 2)) // 3
        card_height = max(88, min(116, panel_rect.height - 240))
        card_top = panel_rect.y + 148
        for index, variant in enumerate(ability.variants):
            card_x = panel_rect.x + 28 + (index * (card_width + gap))
            card_rect = pygame.Rect(card_x, card_top, card_width, card_height)
            pygame.draw.rect(surface, (32, 36, 44), card_rect, border_radius=8)
            pygame.draw.rect(surface, (84, 94, 110), card_rect, width=1, border_radius=8)

            variant_lines = wrap_text(
                small_font,
                variant.description,
                max_width=card_rect.width - 20,
            )
            for line_index, line in enumerate(variant_lines[:4]):
                rendered = small_font.render(line, True, (192, 196, 204))
                surface.blit(
                    rendered,
                    (card_rect.x + 10, card_rect.y + 14 + (line_index * 18)),
                )

        self._draw_detail_nav(surface, body_font, profile)

    def _draw_grid_entry(
        self,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
        rect: pygame.Rect,
        *,
        title: str,
        subtitle: str,
        sprite: pygame.Surface | None,
        selected: bool,
        hovered: bool,
        unlocked: bool,
        accent_color: tuple[int, int, int] | None = None,
    ) -> None:
        bg = (34, 38, 46)
        border = (88, 96, 108)
        if hovered:
            bg = (52, 58, 70)
            border = (140, 150, 165)
        if selected:
            bg = (64, 72, 86)
            border = (255, 235, 120)
        elif unlocked and accent_color is not None:
            border = accent_color

        pygame.draw.rect(surface, bg, rect, border_radius=10)
        pygame.draw.rect(surface, border, rect, width=2, border_radius=10)
        if unlocked and accent_color is not None:
            accent_rect = pygame.Rect(rect.x, rect.y, rect.width, 8)
            pygame.draw.rect(
                surface,
                accent_color,
                accent_rect,
                border_top_left_radius=10,
                border_top_right_radius=10,
            )

        icon_center = (rect.centerx, rect.y + 46)
        if sprite is not None:
            icon_rect = sprite.get_rect(center=icon_center)
            surface.blit(sprite, icon_rect)
        else:
            pygame.draw.circle(surface, (58, 64, 74), icon_center, 26)
            pygame.draw.circle(surface, (96, 104, 118), icon_center, 26, width=2)
            question = body_font.render("?", True, (176, 176, 176))
            surface.blit(question, question.get_rect(center=icon_center))

        title_lines = wrap_text(small_font, title, max_width=rect.width - 14)
        for line_index, line in enumerate(title_lines[:2]):
            rendered = small_font.render(
                line,
                True,
                (225, 225, 225) if unlocked else (175, 175, 175),
            )
            surface.blit(
                rendered,
                rendered.get_rect(center=(rect.centerx, rect.y + 84 + (line_index * 18))),
            )

        if subtitle:
            subtitle_render = small_font.render(subtitle, True, (160, 160, 160))
            surface.blit(
                subtitle_render,
                subtitle_render.get_rect(center=(rect.centerx, rect.bottom - 16)),
            )

    def _draw_detail_panel(
        self,
        *,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
        title: str,
        sprite: pygame.Surface | None,
        stat_lines: list[str],
        detail_lines: list[str],
        detail_title: str,
    ) -> None:
        panel_rect = self._detail_panel_rect(surface)
        pygame.draw.rect(surface, (30, 34, 42), panel_rect, border_radius=12)
        pygame.draw.rect(surface, (108, 116, 128), panel_rect, width=2, border_radius=12)

        title_render = body_font.render(title, True, (235, 235, 235))
        surface.blit(title_render, (panel_rect.x + 28, panel_rect.y + 24))

        if sprite is not None:
            sprite_rect = sprite.get_rect(center=(panel_rect.x + 116, panel_rect.y + 118))
            surface.blit(sprite, sprite_rect)

        left_x = panel_rect.x + 28
        stats_y = panel_rect.y + 190
        stats_title = small_font.render("Stats", True, (180, 180, 180))
        surface.blit(stats_title, (left_x, stats_y))
        for index, line in enumerate(stat_lines):
            rendered = body_font.render(line, True, (225, 225, 225))
            surface.blit(rendered, (left_x, stats_y + 30 + (index * 30)))

        right_x = panel_rect.x + max(240, panel_rect.width // 2)
        detail_title_render = small_font.render(detail_title, True, (180, 180, 180))
        surface.blit(detail_title_render, (right_x, panel_rect.y + 78))
        for index, line in enumerate(detail_lines):
            if not line:
                continue
            rendered = body_font.render(line, True, (220, 220, 220))
            surface.blit(rendered, (right_x, panel_rect.y + 108 + (index * 24)))

    def _draw_detail_nav(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        profile: PlayerProfile,
    ) -> None:
        has_multiple = len(self._discovered_entry_ids_for_active_tab(profile)) > 1
        prev_rect = self._detail_prev_rect(surface)
        self._draw_button(
            surface,
            font,
            prev_rect,
            "Prev",
            selected=self.focus_area == "detail_prev",
            hovered=self.hover_prev_entry,
            enabled=has_multiple,
        )
        self._draw_button(
            surface,
            font,
            self._detail_next_rect(surface),
            "Next",
            selected=self.focus_area == "detail_next",
            hovered=self.hover_next_entry,
            enabled=has_multiple,
        )

    def _entries_for_tab(
        self,
        tab_id: str,
    ) -> list[EnemyProfile | BlessingDefinition | ActiveAbilityDefinition]:
        if tab_id == TAB_ENEMIES:
            return self.enemy_profiles
        if tab_id == TAB_BLESSINGS:
            return self.blessings
        return self.active_abilities

    def _active_tab_id(self) -> str:
        return self.tabs[self.selected_tab_index].tab_id

    def _open_detail_if_unlocked(
        self,
        *,
        tab_id: str,
        index: int,
        encountered_enemy_ids: set[str],
        encountered_blessing_ids: set[str],
    ) -> str | None:
        entries = self._entries_for_tab(tab_id)
        if not (0 <= index < len(entries)):
            return None
        entry = entries[index]
        if tab_id == TAB_ENEMIES:
            enemy = entry if isinstance(entry, EnemyProfile) else None
            if enemy is None or enemy.profile_id not in encountered_enemy_ids:
                return None
            self.detail_entry_id = enemy.profile_id
            self.focus_area = "detail_next"
            return None

        if tab_id == TAB_ABILITIES:
            ability = entry if isinstance(entry, ActiveAbilityDefinition) else None
            if ability is None:
                return None
            self.detail_entry_id = ability.ability_id
            self.focus_area = "detail_next"
            return None

        blessing = entry if isinstance(entry, BlessingDefinition) else None
        if blessing is None or blessing.blessing_id not in encountered_blessing_ids:
            return None
        self.detail_entry_id = blessing.blessing_id
        self.focus_area = "detail_next"
        return None

    def _handle_grid_navigation(
        self,
        actions: MenuActions,
        surface: pygame.Surface,
        tab_id: str,
    ) -> None:
        entries = self._entries_for_tab(tab_id)
        if not entries:
            return

        columns = self._grid_columns(surface)
        current = self.grid_selection_by_tab[tab_id]
        if actions.navigate_left:
            current = max(0, current - 1)
        if actions.navigate_right:
            current = min(len(entries) - 1, current + 1)
        if actions.navigate_up:
            if current - columns >= 0:
                current -= columns
            else:
                self.focus_area = "tabs"
        if actions.navigate_down:
            if current + columns < len(entries):
                current += columns
            else:
                self.focus_area = "back"
        self.grid_selection_by_tab[tab_id] = current

    def _enemy_preview(self, enemy_id: str) -> pygame.Surface | None:
        if enemy_id in self._enemy_preview_cache:
            return self._enemy_preview_cache[enemy_id]

        clip = self.enemy_library.get_animation_clip(enemy_id)
        if clip is None or not clip.frames:
            self._enemy_preview_cache[enemy_id] = None
            return None

        preview = pixelart_upscale_surface(clip.frames[0], 2)
        self._enemy_preview_cache[enemy_id] = preview
        return preview

    def _ability_preview(
        self,
        ability: ActiveAbilityDefinition,
        *,
        target_size: int,
    ) -> pygame.Surface | None:
        cache_key = f"{ability.ability_id}:{int(target_size)}"
        cached = self._ability_preview_cache.get(cache_key)
        if cached is not None:
            return cached

        preview = self._build_ability_preview_surface(ability)
        if preview is None:
            self._ability_preview_cache[cache_key] = None
            return None

        width, height = preview.get_size()
        max_dim = max(width, height)
        if max_dim <= 0:
            self._ability_preview_cache[cache_key] = None
            return None

        scale = float(target_size) / float(max_dim)
        scaled = pygame.transform.scale(
            preview,
            (
                max(1, int(round(width * scale))),
                max(1, int(round(height * scale))),
            ),
        )
        self._ability_preview_cache[cache_key] = scaled
        return scaled

    def _build_ability_preview_surface(
        self,
        ability: ActiveAbilityDefinition,
    ) -> pygame.Surface | None:
        if ability.logbook_preview_icon_path:
            icon_path = (PROJECT_ROOT / ability.logbook_preview_icon_path).resolve()
            return load_pixelart_image(icon_path, scale_multiple=4)

        if ability.logbook_preview_effect_id:
            clip = self.effect_library.get_clip(ability.logbook_preview_effect_id)
            if clip is None or not clip.frames:
                return None

            frame = clip.frames[-1] if ability.logbook_preview_frame == "last" else clip.frames[0]
            return frame.copy()

        return None

    def _enemy_tier_color(self, tier: EnemyTier) -> tuple[int, int, int]:
        if tier is EnemyTier.ELITE:
            return (156, 92, 224)
        if tier is EnemyTier.BOSS:
            return (230, 190, 80)
        return (128, 132, 138)

    def _enemy_ability_detail_lines(
        self,
        enemy: EnemyProfile,
        font: pygame.font.Font,
    ) -> list[str]:
        if not enemy.abilities:
            return ["No special abilities recorded."]

        lines: list[str] = []
        for ability in enemy.abilities:
            if lines:
                lines.append("")
            lines.append(ability.display_name)
            description_lines = wrap_text(
                font,
                ability.description or "No description recorded.",
                max_width=360,
            )
            lines.extend(description_lines)
        return lines

    @staticmethod
    def _advance_looping_animation(
        state: TimedEffectAnimationState,
        *,
        fps: float,
        frame_count: int,
        render_dt: float,
    ) -> None:
        if frame_count <= 0:
            return

        frame_duration = 1.0 / max(0.01, fps)
        state.frame_progress_seconds += max(0.0, render_dt)
        while state.frame_progress_seconds >= frame_duration:
            state.frame_progress_seconds -= frame_duration
            state.frame_index = (state.frame_index + 1) % frame_count

    def _discovered_entry_ids_for_active_tab(self, profile: PlayerProfile) -> list[str]:
        if self._active_tab_id() == TAB_ENEMIES:
            return [
                enemy.profile_id
                for enemy in self.enemy_profiles
                if enemy.profile_id in profile.logbook.encountered_enemy_ids
            ]
        if self._active_tab_id() == TAB_BLESSINGS:
            return [
                blessing.blessing_id
                for blessing in self.blessings
                if blessing.blessing_id in profile.logbook.encountered_blessing_ids
            ]
        return [ability.ability_id for ability in self.active_abilities]

    def _cycle_detail_entry(self, profile: PlayerProfile, *, step: int) -> None:
        discovered_entries = self._discovered_entry_ids_for_active_tab(profile)
        if len(discovered_entries) <= 1 or self.detail_entry_id is None:
            return
        try:
            current_index = discovered_entries.index(self.detail_entry_id)
        except ValueError:
            self.detail_entry_id = discovered_entries[0]
            return
        self.detail_entry_id = discovered_entries[(current_index + step) % len(discovered_entries)]

    def _tab_rects(self, surface: pygame.Surface) -> list[pygame.Rect]:
        width = 170
        height = 42
        gap = 16
        total_width = (len(self.tabs) * width) + ((len(self.tabs) - 1) * gap)
        start_x = (surface.get_width() - total_width) // 2
        y = 130
        return [
            pygame.Rect(start_x + index * (width + gap), y, width, height)
            for index in range(len(self.tabs))
        ]

    def _grid_columns(self, surface: pygame.Surface) -> int:
        return max(3, min(5, surface.get_width() // 200))

    def _grid_rects(self, surface: pygame.Surface, entry_count: int) -> list[pygame.Rect]:
        columns = self._grid_columns(surface)
        cell_width = 146
        cell_height = 126
        gap_x = 16
        gap_y = 16
        total_width = (columns * cell_width) + ((columns - 1) * gap_x)
        start_x = max(36, (surface.get_width() - total_width) // 2)
        start_y = 190
        rects: list[pygame.Rect] = []
        for index in range(entry_count):
            row = index // columns
            col = index % columns
            rects.append(
                pygame.Rect(
                    start_x + col * (cell_width + gap_x),
                    start_y + row * (cell_height + gap_y),
                    cell_width,
                    cell_height,
                )
            )
        return rects

    def _back_rect(self, surface: pygame.Surface) -> pygame.Rect:
        return pygame.Rect(
            (surface.get_width() - 240) // 2,
            surface.get_height() - 76,
            240,
            42,
        )

    def _detail_panel_rect(self, surface: pygame.Surface) -> pygame.Rect:
        return pygame.Rect(110, 200, surface.get_width() - 220, surface.get_height() - 360)

    def _detail_prev_rect(self, surface: pygame.Surface) -> pygame.Rect:
        panel_rect = self._detail_panel_rect(surface)
        return pygame.Rect(panel_rect.right - 188, panel_rect.y + 18, 76, 36)

    def _detail_next_rect(self, surface: pygame.Surface) -> pygame.Rect:
        panel_rect = self._detail_panel_rect(surface)
        return pygame.Rect(panel_rect.right - 100, panel_rect.y + 18, 76, 36)

    @staticmethod
    def _draw_button(
        surface: pygame.Surface,
        font: pygame.font.Font,
        rect: pygame.Rect,
        label: str,
        *,
        selected: bool,
        hovered: bool,
        enabled: bool = True,
    ) -> None:
        bg = (34, 38, 46)
        border = (88, 96, 108)
        text_color = (225, 225, 225)
        if not enabled:
            bg = (26, 29, 36)
            border = (68, 72, 80)
            text_color = (110, 110, 110)
        if hovered:
            bg = (52, 58, 70)
            border = (140, 150, 165)
        if selected:
            bg = (64, 72, 86)
            border = (255, 235, 120)

        pygame.draw.rect(surface, bg, rect, border_radius=8)
        pygame.draw.rect(surface, border, rect, width=2, border_radius=8)
        rendered = font.render(label, True, text_color)
        surface.blit(rendered, rendered.get_rect(center=rect.center))
