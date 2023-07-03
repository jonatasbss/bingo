import random
import tkinter as tk
from PIL import Image, ImageTk
import imageio
import pygame
from ttkthemes import ThemedTk

letras = ['B', 'I', 'N', 'G', 'O']
intervalos = [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)]
numeros_chamados = []
letra = ''
numero = 0
roleta_gif_images = []


def gerar_numero():
    if len(numeros_chamados) == 75:
        return None  # Todos os números foram chamados

    while True:
        letra_index = random.randint(0, 4)
        min_num, max_num = intervalos[letra_index]
        numero = random.randint(min_num, max_num)
        if numero not in numeros_chamados:
            numeros_chamados.append(numero)
            return letras[letra_index], numero


def chamar_numero():
    resultado = gerar_numero()
    if resultado is not None:
        global letra, numero
        letra, numero = resultado
        mostrar_animacao_roleta()
        tocar_audio()
        btn_chamar.config(text="Novo Número", command=chamar_novo_numero)


def mostrar_animacao_roleta():
    global roleta_gif_images  # Usar a lista global para armazenar as imagens do GIF

    roleta_gif = "img/roleta.gif"  # Substitua "roleta.gif" pelo caminho do seu arquivo GIF
    roleta_frames = imageio.mimread(roleta_gif)
    roleta_frames = [Image.fromarray(frame) for frame in roleta_frames]

    roleta_width, roleta_height = roleta_frames[0].size
    resized_width = 400
    resized_height = int(roleta_height * resized_width / roleta_width)

    roleta_frames = [frame.resize((resized_width, resized_height), Image.BILINEAR) for frame in roleta_frames]

    roleta_gif_images = []
    for frame in roleta_frames:
        roleta_gif_images.append(ImageTk.PhotoImage(frame))

    def mostrar_proximo_frame(frame_index):
        lbl_roleta.config(image=roleta_gif_images[frame_index])

        if frame_index < len(roleta_gif_images) - 1:
            frame_index += 1
            lbl_roleta.after(100, mostrar_proximo_frame, frame_index)
        else:
            mostrar_numero()

    lbl_roleta.config(image=roleta_gif_images[0])
    mostrar_proximo_frame(0)


def mostrar_numero():
    lbl_roleta_bolinha.config(text=f"{letra} - {numero}")
    lbl_roleta_bolinha.config(font=("Arial", 32, "bold"))
    lbl_roleta_bolinha.pack(pady=80)
    lbl_roleta.pack_forget()  # Oculta o label do GIF


def tocar_audio():
    pygame.mixer.music.load("audio/roleta.mp3")  # Substitua "bingo_sound.mp3" pelo caminho do seu arquivo de áudio
    pygame.mixer.music.play()


def chamar_novo_numero():
    # btn_chamar.config(state=tk.DISABLED)
    lbl_roleta.pack()  # Exibe o label do GIF novamente
    chamar_numero()


pygame.mixer.init()

root = ThemedTk(theme="bootstrap")
root.title("Bingo")
root.geometry("600x400")

frame = tk.Frame(root, bg="white")
frame.pack(expand=True, padx=20, pady=20)

lbl_roleta = tk.Label(frame, bg="white")
lbl_roleta.pack(pady=20)

lbl_roleta_bolinha = tk.Label(frame, font=("Arial", 16, "bold"), bg="white")

btn_chamar = tk.Button(frame, text="Chamar número", command=chamar_numero)
btn_chamar.pack(pady=20)

root.mainloop()
