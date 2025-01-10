import tkinter as tk
import subprocess


class NowPlayingWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Now Playing")
        self.root.overrideredirect(True)  # Убирает стандартные элементы окна
        self.root.geometry(self.calculate_position(500, 100))  # Устанавливает размеры и позицию
        self.root.config(bg="black")

        # Метка для отображения информации о треке
        self.label = tk.Label(
            self.root,
            text="Now Playing: Loading...",
            font=("Arial", 14),
            fg="white",
            bg="black",
            wraplength=480,
            justify="center",
        )
        self.label.pack(expand=True, fill="both")

        # Обновление информации каждые 2 секунды
        self.update_track()

    def calculate_position(self, width, height):
        """Вычисляет положение окна внизу по центру."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = screen_height - height - 10  # Отступ 10 пикселей от нижнего края
        return f"{width}x{height}+{x}+{y}"

    def get_now_playing(self):
        """Получает информацию о текущем треке с помощью playerctl."""
        try:
            title = subprocess.check_output(
                ["playerctl", "metadata", "title"], text=True
            ).strip()
            artist = subprocess.check_output(
                ["playerctl", "metadata", "artist"], text=True
            ).strip()
            return f"🎵 {title} - {artist}" if title and artist else "No track playing"
        except subprocess.CalledProcessError:
            return "Player not running"

    def update_track(self):
        """Обновляет отображение трека."""
        now_playing = self.get_now_playing()
        self.label.config(text=now_playing)
        self.root.after(2000, self.update_track)


if __name__ == "__main__":
    root = tk.Tk()
    app = NowPlayingWidget(root)
    root.mainloop()
