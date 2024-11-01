import tkinter as tk
from creatures import Human


class HumanVisualizer:
    def __init__(self, root, human):
        self.root = root
        self.human = human
        self.labels = {}
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Human Visualizer")
        self.root.geometry("400x600")
        self.update_labels()

        # Add Next button
        next_button = tk.Button(self.root, text="Next", command=self.update_human)
        next_button.grid(row=100, column=0, pady=10)

    def update_labels(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        row = 0
        # add the body object
        body_text = f"Body: HP={self.human.hp}, Sustenance={self.human.sustenance}, Dead={self.human.dead}, Decay={self.human.decay}"
        body_label = tk.Label(self.root, text=body_text)
        body_label.grid(row=row, column=0, sticky="w")
        self.labels["body"] = body_label
        row += 1
        for part in self.human.parts:
            row = self.add_parts(part, row, 0)

    def create_label(self, part, row, indent=0):
        label_text = f"{' ' * indent}{part.name}: HP={part.hp}, Armor={part.armor}, Sustenance={part.sustenance}, Dead={part.dead}, Decay={part.decay}"
        label = tk.Label(self.root, text=label_text)
        label.grid(row=row, column=0, sticky="w")
        self.labels[part.name] = label

    def update_human(self):
        self.human.tick()
        self.update_labels()

    def add_parts(self, part, row, indent):
        self.create_label(part, row, indent)
        for attached_part in part.attached_body_parts:
            row = self.add_parts(attached_part, row + 1, indent + 10)
        return row



if __name__ == "__main__":
    root = tk.Tk()
    human = Human(0, 0)
    visualizer = HumanVisualizer(root, human)
    root.mainloop()