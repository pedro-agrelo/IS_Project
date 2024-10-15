import wx

# Class for the main frame (window)
class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        # Set up the panel inside the frame
        panel = MyPanel(self)

        # Set frame size and title
        self.SetSize((350, 200))
        self.SetTitle("Simple Window with wxPython")

# Class for the panel that holds the text and button
class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Create a text box (welcome text)
        self.text_ctrl = wx.TextCtrl(self, pos=(10, 10), size=(300, 30))

        # Add the button to the panel
        my_button = MyButton(self, label="Click Me", pos=(10, 50))

        # Bind the button's click event to a method
        my_button.Bind(wx.EVT_BUTTON, self.on_button_click)

    # Event handler for button click
    def on_button_click(self, event):
        # Get the text from the text box
        user_input = self.text_ctrl.GetValue()

        # Show a message with the entered text
        wx.MessageBox(f"You typed: {user_input}", "Message")

# Class for the button (could be extended in the future)
class MyButton(wx.Button):
    def __init__(self, parent, *args, **kw):
        super(MyButton, self).__init__(parent, *args, **kw)

# Main function to initialize and run the wxPython app
def main():
    app = wx.App(False)  # Don't redirect stdout/stderr
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()
