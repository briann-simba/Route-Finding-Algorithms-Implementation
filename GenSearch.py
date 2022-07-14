import os
import webbrowser
from tkinter import *
from tkinter import messagebox
import folium
import json
from geopy import distance, Nominatim
import requests
from Graph import Graph
from Vertex import Vertex
from search import a_star_search, breadth_first_search, depth_first_search, reconstruct_path
import uuid
# Define the geocoder and add markers for our towns
geocoder = Nominatim(user_agent="search")
_, kenya = geocoder.geocode("Kenya")
kenya = list(kenya)
global general_map
general_map = folium.Map(location=kenya, zoom_start=6)

start_town = ['Kisumu', 'Eldoret', 'Nakuru', 'Nairobi', 'Thika', 'Mombasa','Isiolo','Garissa','Kitui','Malindi']
goal_town = ['Kisumu', 'Eldoret', 'Nakuru', 'Nairobi', 'Thika', 'Mombasa','Isiolo','Garissa','Kitui','Malindi']
algorithms = ['Breadth First Search', 'Depth First Search', 'A* Search']

# store locations as a dictionary
town_locations = dict()

#function to visualize line on map
def visualize(path, map_to_draw_on=general_map):
    points = list(map(lambda n: town_locations[n], path))
    folium.PolyLine(points,color="red").add_to(map_to_draw_on)

              
#function to generate points on map              
def populate():
    for town in start_town:
        _, loc = geocoder.geocode(f"{town}, Kenya")
        
        loc = list(loc)
        town_locations[town] = loc
        folium.Marker(location = loc,popup = town,icon=folium.Icon(color="red")).add_to(general_map)

populate()


# Make a  Graph of 10 towns.

kisumu = Vertex('Kisumu')
eldoret = Vertex('Eldoret')
nakuru = Vertex('Nakuru')
thika = Vertex('Thika')
malindi = Vertex('Malindi')
nairobi = Vertex('Nairobi')
kitui = Vertex('Kitui')
isiolo = Vertex('Isiolo')
garissa = Vertex('Garissa')
mombasa = Vertex('Mombasa')

graph = Graph()
graph.addVertex(kisumu)
graph.addVertex(nairobi)
graph.addVertex(eldoret)
graph.addVertex(nakuru)
graph.addVertex(thika)
graph.addVertex(mombasa)
graph.addVertex(garissa)
graph.addVertex(isiolo )
graph.addVertex(malindi)
graph.addVertex(kitui)


# create edge
graph.addDirectedEdge(kisumu, eldoret)
graph.addDirectedEdge(eldoret, kisumu)
graph.addDirectedEdge(kisumu, nakuru)
graph.addDirectedEdge(nakuru, kisumu)
graph.addDirectedEdge(eldoret, nakuru)
graph.addDirectedEdge(nakuru, eldoret)
graph.addDirectedEdge(eldoret, nairobi)
graph.addDirectedEdge(nairobi, eldoret)
graph.addDirectedEdge(isiolo, thika)
graph.addDirectedEdge(thika, isiolo)
graph.addDirectedEdge(nakuru, nairobi)
graph.addDirectedEdge(nairobi, nakuru)
graph.addDirectedEdge(nairobi, thika)
graph.addDirectedEdge(thika, nairobi)
graph.addDirectedEdge(nairobi, mombasa)
graph.addDirectedEdge(mombasa, nairobi)
graph.addDirectedEdge(kitui, mombasa)
graph.addDirectedEdge(mombasa,kitui)
graph.addDirectedEdge(nairobi, garissa)
graph.addDirectedEdge(garissa,nairobi)
graph.addDirectedEdge(nairobi,isiolo)
graph.addDirectedEdge(nairobi,isiolo)
graph.addDirectedEdge(garissa,isiolo)
graph.addDirectedEdge(isiolo,garissa)
graph.addDirectedEdge(isiolo,kitui)
graph.addDirectedEdge(kitui,isiolo)
graph.addDirectedEdge(garissa,kitui)
graph.addDirectedEdge(kitui,garissa)
graph.addDirectedEdge(nairobi,kitui)
graph.addDirectedEdge(kitui,nairobi)
graph.addDirectedEdge(kitui,malindi)
graph.addDirectedEdge(malindi,kitui)
graph.addDirectedEdge(garissa,malindi)
graph.addDirectedEdge(malindi,garissa)
graph.addDirectedEdge(mombasa,malindi)
graph.addDirectedEdge(malindi,mombasa)
def town_index(town_name, towns):
    return graph.vertices.index(list(filter(lambda n: n.value == town_name, towns.vertices))[0])
def get_distance(path):
    global total_distance_travelled
    total_distance_travelled=0
    for i in range(len(path)-1):
        x = path[i]
        y = path[i+1]
        _, x_loc = geocoder.geocode(x)
        _, y_loc = geocoder.geocode(y)
        resp=requests.get(f'http://router.project-osrm.org/route/v1/driving/{x_loc[1]},{x_loc[0]};{y_loc[1]},{y_loc[0]}?overview=false')
        distance=((json.loads(resp.content))["routes"][0]["distance"])*0.001
        total_distance_travelled+=distance 
    return total_distance_travelled                                    
def on_click():
     filename = str(uuid.uuid4())
     print(filename)
     global algo,start,goal,next_button
     print(algo.get(),start.get(),goal.get())
     if "Breadth First Search" == algo.get():
         path = breadth_first_search(graph.vertices[town_index(goal.get(), graph)], graph, town_index(start.get(), graph))
         print(path)
         visualize(list(map(lambda n: n.value, path)))
         next_button.config(state="disabled")
         general_map.save(f"{filename}.html")
         messagebox.showinfo('Distance',str(get_distance(path)))
         url = f"file:///C:/Users/Hp/PingPong/{filename}.html"
         webbrowser.open(url,new=2)
         root.destroy()
         os.system('python Gensearch.py')    
     elif "Depth First Search" == algo.get():
         path = depth_first_search(graph.vertices[town_index(goal.get(), graph)], graph, town_index(start.get(), graph))
         visualize(list(map(lambda n: n.value, path)))
         next_button.config(state="disabled")
         general_map.save(f"{filename}.html")
         messagebox.showinfo('Distance',str(get_distance(path)))
         url = f"file:///C:/Users/Hp/PingPong/{filename}.html"
         webbrowser.open(url,new=2)
         root.destroy()
         os.system('python Gensearch.py')     
     else:
        came_from, cost = a_star_search(graph, graph.vertices[town_index(goal.get(), graph)], town_index(start.get(), graph))
        print(cost)
        path = reconstruct_path(came_from, graph.vertices[town_index(start.get(), graph)].value, graph.vertices[town_index(goal.get(), graph)].value)
        print(path)
        visualize(list(filter(lambda n: not isinstance(n, int), path)))
        next_button.config(state="disabled")
        general_map.save(f"{filename}.html")
        messagebox.showinfo('Distance',str(get_distance(path)))
        url = f"file:///C:/Users/Hp/PingPong/{filename}.html"
        webbrowser.open(url,new=2)
        root.destroy()
        os.system('python Gensearch.py')
            
root = Tk() #create the tkinter window
bg = PhotoImage(file = "kenya2.png")
labela = Label(root,image=bg)
labela.place(x=300, y=0)
root.title("DFS,BFS,and A* Route Finding")
root.geometry("1380x1380")
algo = StringVar(root)
start = StringVar(root)
goal = StringVar(root)
algo.set("Breadth First Search")
start.set('Kisumu')
goal.set('Mombasa')
algorithm_menu = OptionMenu(root,algo,"Breadth First Search", "Depth First Search", "A* Search")
Label(root, text="\n Search Algorithm").pack()
algorithm_menu.pack()
Label(root, text="\n Start Town").pack()
start_menu = OptionMenu(root, start,'Kisumu', 'Eldoret', 'Nakuru', 'Nairobi', 'Thika', 'Mombasa','Isiolo','Garissa','Kitui','Malindi')
start_menu.pack()
Label(root, text="\n Goal Town").pack()
goal_menu = OptionMenu(root, goal,'Kisumu', 'Eldoret', 'Nakuru', 'Nairobi', 'Thika', 'Mombasa','Isiolo','Garissa','Kitui','Malindi')
goal_menu.pack()
algorithm_menu.pack()
next_button = Button(root,text="Get Route",command=on_click)
next_button.pack()
reset_button = Button(root,text="Reset",command=root.destroy)
reset_button.pack()
root.mainloop()