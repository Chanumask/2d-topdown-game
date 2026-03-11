import pygame


def build_centered_menu_rects(
    surface: pygame.Surface,
    font: pygame.font.Font,
    options: list[str],
    start_y: int,
    row_height: int,
    min_width: int = 280,
) -> list[pygame.Rect]:
    rects: list[pygame.Rect] = []
    center_x = surface.get_width() // 2

    for index, option in enumerate(options):
        text_width, text_height = font.size(option)
        width = max(min_width, text_width + 64)
        height = max(text_height + 16, row_height - 6)
        center_y = start_y + (index * row_height)
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (center_x, center_y)
        rects.append(rect)

    return rects


def hovered_index(
    mouse_position: tuple[int, int] | None,
    rects: list[pygame.Rect],
) -> int | None:
    if mouse_position is None:
        return None
    for index, rect in enumerate(rects):
        if rect.collidepoint(mouse_position):
            return index
    return None


def draw_centered_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    y: int,
    color: tuple[int, int, int],
) -> None:
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(rendered, rect)


def draw_menu_buttons(
    surface: pygame.Surface,
    font: pygame.font.Font,
    options: list[str],
    rects: list[pygame.Rect],
    selected_index: int,
    hover_index: int | None,
    normal_color: tuple[int, int, int],
    selected_color: tuple[int, int, int],
) -> None:
    for index, option in enumerate(options):
        if index >= len(rects):
            break

        rect = rects[index]
        is_selected = index == selected_index
        is_hovered = index == hover_index

        if is_selected:
            background = (64, 72, 86)
            border = (255, 235, 120)
            text_color = selected_color
        elif is_hovered:
            background = (52, 58, 70)
            border = (140, 150, 165)
            text_color = selected_color
        else:
            background = (34, 38, 46)
            border = (88, 96, 108)
            text_color = normal_color

        pygame.draw.rect(surface, background, rect, border_radius=8)
        pygame.draw.rect(surface, border, rect, width=2, border_radius=8)

        rendered = font.render(option, True, text_color)
        rendered_rect = rendered.get_rect(center=rect.center)
        surface.blit(rendered, rendered_rect)


def wrap_text(font: pygame.font.Font, text: str, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]

    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word

    lines.append(current)
    return lines
