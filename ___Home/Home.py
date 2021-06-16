def run(tk, app_frame):
    print(f'{app_frame.winfo_width()}, {app_frame.winfo_height()}')
    for i in range(100):
        tk.Label(app_frame, text="app ran").grid(row=i, column=0)
