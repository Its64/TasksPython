import flet as ft
from io import StringIO 
import sys
import json

tasks = {} # здесь будут храниться задачи

with open('test.json') as f:
  tasks = json.load(f)

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def main(page: ft.Page):
    page.title = "Program"
    page.window_height = 750
    page.window_width = 900

    task_count = 0 # Задание по счету в категории
    task = {} # Задание прямо сейчас
    task_type = "var" # Выбранная категория
    tasks_main = {} # Задания в выбранной категории

    def next_task(args): # Переключение на след. задание в категории
      nonlocal task_count
      task_count += 1
      print(task)
      update()
      page.update()

    def change(e):
      nonlocal task_type
      nonlocal task_count
      task_count = 0
      task_type = e
      update()

    def update(): # Обновление задания
      nonlocal task_count
      nonlocal task
      nonlocal task_type
      nonlocal tasks_main
      nonlocal task_text

      match task_type:
        case "var":
          tasks_main = tasks["var"]
        case "func":
          tasks_main = tasks["func"]
        case "if":
          tasks_main = tasks["if"]
        case "while":
          tasks_main = tasks["while"]
        case "arr":
          tasks_main = tasks["arr"]
      
      task = tasks_main[str(task_count)]
      task_text.value = task["task"]
      code.value = ""
      page.update()

    match task_type:
      case "var":
        tasks_main = tasks["var"]
      case "func":
        tasks_main = tasks["func"]
      case "if":
        tasks_main = tasks["if"]
      case "while":
        tasks_main = tasks["while"]
    
    task = tasks_main[str(task_count)]
    print(task)

    task_text = ft.Text( # Текст задачи
      value=task["task"],
      style="headlineMedium"
    )

    code = ft.TextField( # Ввод кода
      value="# Write your code.",
      multiline=True,
      min_lines=15,
      max_lines=15,
    )

    def run(args=False): # Запуск кода
        try:
          with Capturing() as output: # Запись вывода кода
            exec(code.value)
            try:
              test1 = eval(task["test1"]["if"])
              test2 = eval(task["test2"]["if"])
              test3 = eval(task["test3"]["if"])
            except:
              pass

          print("Running")
          exec(code.value)

          output_final = ""

          test1 = False
          test2 = False
          test3 = False

          try:
            test1 = eval(task["test1"]["if"])
            test2 = eval(task["test2"]["if"])
            test3 = eval(task["test3"]["if"])
          except:
            pass

          print(test1, test2, test3)
          if test1 == True and test2 == True and test3 == True:
            output_final += "Success!\n"
          else:
            output_final += "Wrong\n"

          for i in output:
            output_final += i + "\n"

          output_text.value = output_final
          page.update()
        except:
          with Capturing() as output:
            print("Error")
          output_text.value = output
          page.update()

    output_text = ft.Text(value="Output")

    page.add(
        ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Variables",
                    bgcolor=ft.colors.BLUE_GREY_100,
                    color=ft.colors.BLACK,
                    expand=1,
                    on_click=lambda e: change("var"),
                ),
                ft.ElevatedButton(
                    text="Functions",
                    bgcolor=ft.colors.BLUE_GREY_100,
                    color=ft.colors.BLACK,
                    expand=1,
                    on_click=lambda e: change("func"),
                ),
                ft.ElevatedButton(
                    text="If, else",
                    bgcolor=ft.colors.BLUE_GREY_100,
                    color=ft.colors.BLACK,
                    expand=1,
                    on_click=lambda e: change("if"),
                ),
                ft.ElevatedButton(
                    text="Lists",
                    bgcolor=ft.colors.BLUE_GREY_100,
                    color=ft.colors.BLACK,
                    expand=1,
                    on_click=lambda e: change("arr"),
                ),
                ft.ElevatedButton(
                    text="While, for",
                    bgcolor=ft.colors.BLUE_GREY_100,
                    color=ft.colors.BLACK,
                    expand=1,
                    on_click=lambda e: change("while"),
                ),
            ]
        )
    )

    page.add(task_text)

    page.add(code)

    page.add(
        ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Run",
                    bgcolor=ft.colors.BLUE_GREY_100,
                    color=ft.colors.BLACK,
                    on_click=run,
                ),
                ft.ElevatedButton(
                    text="Next task",
                    bgcolor=ft.colors.BLUE_GREY_100,
                    color=ft.colors.BLACK,
                    on_click=next_task,
                    # data=0,
                ),
            ]
        )
    )

    page.add(output_text)

ft.app(target=main)