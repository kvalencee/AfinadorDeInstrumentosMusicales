"""
Custom Button Widget for macOS
Creates buttons with custom colors that work on macOS
"""

import tkinter as tk


class CustomButton(tk.Frame):
    """Custom button widget that supports bg and fg colors on macOS"""
    
    def __init__(self, parent, text="", command=None, bg="#ffffff", fg="#000000", 
                 activebackground=None, activeforeground=None, font=None, 
                 padx=10, pady=5, cursor="hand2", state="normal", **kwargs):
        super().__init__(parent, bg=bg, cursor=cursor, **kwargs)
        
        self.bg = bg
        self.fg = fg
        self.activebackground = activebackground or bg
        self.activeforeground = activeforeground or fg
        self.command = command
        self.state_var = state
        
        # Create label inside frame
        self.label = tk.Label(
            self,
            text=text,
            bg=bg,
            fg=fg,
            font=font,
            cursor=cursor if state == "normal" else "arrow",
            padx=padx,
            pady=pady
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        # Bind events for hover and click
        if state == "normal":
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)
            self.bind("<Button-1>", self._on_click)
            self.label.bind("<Enter>", self._on_enter)
            self.label.bind("<Leave>", self._on_leave)
            self.label.bind("<Button-1>", self._on_click)
        else:
            self.configure(bg="#cccccc")
            self.label.configure(bg="#cccccc", fg="#666666")
    
    def _on_enter(self, event):
        """Mouse hover effect"""
        if self.state_var == "normal":
            self.configure(bg=self.activebackground)
            self.label.configure(bg=self.activebackground, fg=self.activeforeground)
    
    def _on_leave(self, event):
        """Mouse leave effect"""
        if self.state_var == "normal":
            self.configure(bg=self.bg)
            self.label.configure(bg=self.bg, fg=self.fg)
    
    def _on_click(self, event):
        """Handle click"""
        if self.state_var == "normal" and self.command:
            self.command()
    
    def config(self, **kwargs):
        """Configure button properties"""
        if 'state' in kwargs:
            self.state_var = kwargs['state']
            if self.state_var == "disabled":
                self.configure(bg="#cccccc", cursor="arrow")
                self.label.configure(bg="#cccccc", fg="#666666", cursor="arrow")
            else:
                self.configure(bg=self.bg, cursor="hand2")
                self.label.configure(bg=self.bg, fg=self.fg, cursor="hand2")
        
        if 'text' in kwargs:
            self.label.configure(text=kwargs['text'])
