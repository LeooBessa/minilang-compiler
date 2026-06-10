# app.py — compatível com Flet 3.x
import sys
import flet as ft
from compilador import compilar

def main(page: ft.Page):
    page.title = "MiniLang Compiler"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.width = 900
    page.window.height = 720

    # ── Editor de código ────────────────────────────────────────────────────
    codigo_editor = ft.TextField(
        label="Código fonte (MiniLang)",
        multiline=True,
        min_lines=10,
        max_lines=15,
        value="x = 10\ny = 2\nz = x * y\nw = z - 5\nres = w / 3\nprint(res)",
        expand=True,
        border_color=ft.Colors.BLUE_400,
    )

    # ── Textos de saída ─────────────────────────────────────────────────────
    txt_tokens = ft.Text("", size=12, selectable=True)
    txt_asm    = ft.Text("", size=12, selectable=True)
    txt_out    = ft.Text("", size=12, selectable=True)
    txt_err    = ft.Text("", size=12, selectable=True, color=ft.Colors.RED_300)

    def caixa(titulo, cor, conteudo):
        return ft.Column([
            ft.Text(titulo, weight=ft.FontWeight.BOLD, color=cor, size=13),
            ft.Container(
                content=ft.Column([conteudo], scroll=ft.ScrollMode.AUTO),
                bgcolor=ft.Colors.GREY_900,
                border_radius=8,
                padding=12,
                height=130,
                expand=True,
            ),
        ], spacing=4, expand=True)

    painel_tokens = caixa("1. Tokens (Léxer)",         ft.Colors.BLUE_300,   txt_tokens)
    painel_asm    = caixa("2. Código intermediário",   ft.Colors.PURPLE_300, txt_asm)
    painel_out    = caixa("3. Saída da execução",      ft.Colors.GREEN_300,  txt_out)
    painel_err    = caixa("⚠ Erros",                  ft.Colors.RED_300,    txt_err)

    status_icon = ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.GREY_600, size=14)
    status_txt  = ft.Text("aguardando...", color=ft.Colors.GREY_500, size=12)

    # ── Ação compilar ───────────────────────────────────────────────────────
    def ao_compilar(e):
        codigo = codigo_editor.value.strip()
        if not codigo:
            return

        for t in [txt_tokens, txt_asm, txt_out, txt_err]:
            t.value = ""
        status_txt.value  = "compilando..."
        status_icon.color = ft.Colors.YELLOW_400
        page.update()

        resultado = compilar(codigo)

        txt_tokens.value = "  ".join(resultado["tokens"])

        if resultado["erro_sintatico"]:
            txt_err.value     = "ERRO SINTÁTICO: estrutura inválida."
            status_icon.color = ft.Colors.RED_400
            status_txt.value  = "erro sintático"
        elif resultado["erro_semantico"]:
            txt_err.value     = resultado["erro_semantico"]
            status_icon.color = ft.Colors.RED_400
            status_txt.value  = "erro semântico"
        else:
            txt_asm.value     = "\n".join(resultado["codigo_intermediario"])
            txt_out.value     = resultado["output"].strip()
            status_icon.color = ft.Colors.GREEN_400
            status_txt.value  = "compilação bem-sucedida ✓"

        page.update()

    def ao_limpar(e):
        for t in [txt_tokens, txt_asm, txt_out, txt_err]:
            t.value = ""
        status_icon.color = ft.Colors.GREY_600
        status_txt.value  = "aguardando..."
        page.update()

    # ── Botões ──────────────────────────────────────────────────────────────
    btn_compilar = ft.ElevatedButton(
        "▶  Compilar",
        icon=ft.Icons.PLAY_ARROW,
        on_click=ao_compilar,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        height=44,
    )

    btn_limpar = ft.OutlinedButton(
        "Limpar",
        icon=ft.Icons.CLEAR,
        on_click=ao_limpar,
    )

    # ── Layout ──────────────────────────────────────────────────────────────
    page.add(
        ft.Text("MiniLang Compiler", size=22, weight=ft.FontWeight.BOLD),
        ft.Text("Digite seu código e clique em Compilar.", size=13,
                color=ft.Colors.GREY_400),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        codigo_editor,
        ft.Row([
            btn_compilar,
            btn_limpar,
            ft.Row([status_icon, status_txt], spacing=6),
        ], spacing=10),
        ft.Divider(height=8),
        ft.Row([
            ft.Column([painel_tokens, painel_asm], expand=True, spacing=10),
            ft.Column([painel_out,    painel_err],  expand=True, spacing=10),
        ], spacing=16, expand=True),
    )

# No navegador (GitHub Pages / Pyodide) roda como app estático;
# localmente ou no Docker, sobe como servidor web na porta 8080.
if sys.platform == "emscripten":
    ft.app(main)
else:
    ft.app(main, view=ft.AppView.WEB_BROWSER, port=8080, host="0.0.0.0")