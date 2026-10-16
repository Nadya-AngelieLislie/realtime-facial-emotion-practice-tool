import cv2
import time
from fer import FER
from collections import Counter
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def show_mismatch_gallery(image_paths, match_count, total_frames):
    if not image_paths:
        print(f"Tidak ada mismatch. Skor akhir: {match_count}/{total_frames}")
        return

    index = [0]

    def update_image():
        img = Image.open(image_paths[index[0]])
        img = img.resize((400, 300))
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk
        counter_label.config(text=f"{index[0]+1} dari {len(image_paths)}")

    gallery = tk.Tk()
    gallery.title("Galeri Ekspresi Tidak Cocok")
    gallery.geometry("480x450")

    # Skor akhir
    score_label = tk.Label(gallery, text=f"Hasil kamu: {match_count} cocok dari {total_frames} frame", font=("Helvetica", 11, "bold"))
    score_label.pack(pady=(10, 0))

    img_label = tk.Label(gallery)
    img_label.pack(pady=10)

    counter_label = tk.Label(gallery, text="")
    counter_label.pack()

    btn_frame = tk.Frame(gallery)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="⬅️ Sebelumnya", command=lambda: [index.__setitem__(0, index[0]-1), update_image()] if index[0] > 0 else None).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="➡️ Berikutnya", command=lambda: [index.__setitem__(0, index[0]+1), update_image()] if index[0] < len(image_paths)-1 else None).pack(side=tk.RIGHT, padx=10)

    tk.Button(gallery, text="Tutup", command=gallery.destroy).pack(pady=10)

    update_image()
    gallery.mainloop()

def start_expression_practice(target_emotion):
    detector = FER(mtcnn=True)
    session_duration = 60
    start_time = time.time()
    emotion_window = []
    WINDOW_SIZE = 30
    mismatch_images = []
    total_frames = 0
    match_count = 0

    cap = cv2.VideoCapture(0)
    print(f"🎬 Latihan dimulai untuk emosi: {target_emotion.upper()}! Tekan 'q' untuk berhenti.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.detect_emotions(frame)

        final_emotion = None
        for result in results:
            (x, y, w, h) = result["box"]
            emotions = result["emotions"]
            dominant_emotion = max(emotions, key=emotions.get)

            # Majority voting
            emotion_window.append(dominant_emotion)
            if len(emotion_window) > WINDOW_SIZE:
                emotion_window.pop(0)
            final_emotion = Counter(emotion_window).most_common(1)[0][0]

            # Update skor
            total_frames += 1
            if final_emotion == target_emotion:
                match_count += 1

            # Wajah frontal check
            face_center_x = x + w / 2
            frame_center_x = frame.shape[1] / 2
            offset = abs(face_center_x - frame_center_x)
            if offset > 80:
                cv2.putText(frame, "Arahkan wajah ke kamera", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # Kotak wajah
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Skor emosi
            y_offset = y + h + 20
            for emo, val in emotions.items():
                cv2.putText(frame, f"{emo}: {val:.2f}", (x, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100), 1)
                y_offset += 20

            # Feedback
            match = final_emotion == target_emotion
            feedback = "MATCH" if match else f"Coba ekspresikan '{target_emotion}'"
            color = (0, 255, 0) if match else (0, 0, 255)
            cv2.putText(frame, f"Final: {final_emotion}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            cv2.putText(frame, feedback, (x, y_offset + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Logging
            with open("emotion_log.txt", "a") as f:
                f.write(f"{time.strftime('%H:%M:%S')} - Final: {final_emotion}, Target: {target_emotion}, Match: {match}\n")

            # Simpan screenshot jika mismatch
            if not match:
                filename = f"screenshot_mismatch_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                mismatch_images.append(filename)

        # Tampilkan
        cv2.imshow("Latihan Ekspresi Aktor 🎭", frame)

        # Timer / exit
        if time.time() - start_time > session_duration:
            print("Waktu latihan habis!")
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Latihan dihentikan.")
            break

    cap.release()
    cv2.destroyAllWindows()
    show_mismatch_gallery(mismatch_images, match_count, total_frames)

def open_gui():
    def on_start():
        selected_emotion = emotion_var.get()
        root.destroy()
        start_expression_practice(selected_emotion)

    root = tk.Tk()
    root.title("Pilih Emosi untuk Latihan")
    root.geometry("300x200")

    tk.Label(root, text="🎭 Pilih Emosi Target:").pack(pady=10)

    emotion_var = tk.StringVar(value="neutral")
    emotions = ["happy", "sad", "angry", "fear", "surprise", "disgust", "neutral"]

    dropdown = ttk.Combobox(root, textvariable=emotion_var, values=emotions, state="readonly")
    dropdown.pack(pady=5)

    start_btn = tk.Button(root, text="Mulai Latihan", command=on_start)
    start_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    open_gui()
