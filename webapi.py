import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
r = requests.get(url)
#確認是否連結成功
print("Status code: ", r.status_code)

response_dict = r.json()
#印出有哪些key值可用
print(response_dict.keys())
#印出總數
print("Total repositoreis: " , response_dict["total_count"])

repo_dicts = response_dict["items"]

print("Repositories returned: ", len(repo_dicts))

#觀看其中一個的內容
repo_dict = repo_dicts[0]
print("\nKeys: ", len(repo_dict))


print("\nSelected information about each repository")
names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict["name"])
    #stars.append(repo_dict["stargazers_count"])
    description = repo_dict["description"]
    if not description:
        description = "No description provided."
    plot_dict = {
        "value": repo_dict["stargazers_count"],
        "label": description,
        "xlink": repo_dict["html_url"]
    }

    plot_dicts.append(plot_dict)

my_style = LS("#333366", base_style=LCS)
my_style.title_font_size = 24
my_style.label_font_size = 14
my_style.major_label_font_size = 18

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000
chart = pygal.Bar(my_config, style=my_style)
chart.title = "Most-Starred Python Projects on Guthub"
chart.x_labels = names

chart.add("", plot_dicts)
chart.render_to_file("python_repos.svg")

print("Finish")
