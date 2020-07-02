import tkinter as tk
from tkinter import ttk
import recommendation_system as rec


LARGE_FONT = ("Verdana", 12)

class App(tk.Tk):
    def __init__(self):
        
        tk.Tk.__init__(self)
        self.title("Movie Recommendations")
        
        self.rs = rec.Rs()
        self.current_user = rec.User(0)
        self.rs.users.append(self.current_user)
        # Recommendations
        self.NUM_OF_RECOMMENDATIONS = 5

        self.movie_id = ''
        self.movie_name_var = tk.StringVar()
        self.movie_name = tk.StringVar()
        self.movie_name.set("Currently selected: ")

        self.label = tk.Label(self, text = "Enter a name of a movie you have watched")
        self.label.pack()
        
        self.entry_box = tk.Entry(self, textvariable=self.movie_name_var)
        self.entry_box.pack()
        
        self.select_movie_button = tk.Button(self, text="Select movie",command=self.select_movie)
        self.select_movie_button.pack()

        rate_movie_label = tk.Label(self, text="Rate The Selected Movie")
        rate_movie_label.pack()
        
        self.selected_movie_label = tk.Label(self, textvariable=self.movie_name)
        self.selected_movie_label.pack()

        self.rating = tk.IntVar()
        self.rating.set(0)  

        ratings = [
            ("1 Star",1),
            ("2 Stars",2),
            ("3 Stars",3),
            ("4 Stars",4),
            ("5 Stars",5)
        ]

        for val, rating in enumerate(ratings):
            tk.Radiobutton(self, 
                          text=rating[0],
                          padx = 20, 
                          variable=self.rating,
                          value=val).pack(anchor=tk.W)
        
        self.rate_button = tk.Button(self, text="confirm", command=self.add_rating)
        self.rate_button.pack()

    def add_rating(self):

        if self.movie_name != "Currently selected: ":
            del self.rs.users[-1]
            
            if self.rating.get() >= 3:
                self.current_user.add_movie_liked(self.movie_id,self.rs.movie_instances) #Find the id
            else:
                self.current_user.add_movie_disliked(self.movie_id,self.rs.movie_instances)
            self.rs.users.append(self.current_user)
            self.recommend()
        else:
            t=tk.Tk()
            t.title("Error")
            tk.Label(t,text="There is no movie selected").pack()
            
    def select_movie(self):
        name = self.movie_name_var.get()
        is_movie = False
        
        try:
            self.listbox.pack_forget()
            self.scrollbar.pack_forget()
            self.amount_recommended_label.pack_forget()
            self.movie_recomended_label.pack_forget()
        except:
            pass

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.listbox.config(width=50)
        # dictionary that will contains the function associated to each item
        self.dbclick_cmds = {} 

        self.listbox.insert('end', "Double-Click an movie to select it:")
        self.dbclick_cmds["Double-Click to select a movie"] = lambda: None
        self.dbclick_cmds[''] = lambda: None

        self.listbox.pack(side='left', fill='both')

        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.bind('<Double-1>', self.dbclick)

        for movie in self.rs.movie_instances:
            if str(movie.id) not in self.current_user.get_movies_liked() | self.current_user.get_movies_disliked():

                if name.lower() in movie.name.lower() and movie.name.lower()!='title':
                    is_movie = True
                    n = movie.name
                    self.movie_id = movie.id
                    self.listbox.insert('end', movie.name)
                    self.dbclick_cmds[n] = lambda i=n: self.select_movie_from_lb(i)

        if is_movie:
            self.select_movie_from_lb(n)# Error check for if this is not a movie
        else:
            r=tk.Tk()
            r.title("Error")
            tk.Label(r,text = "No movies found with similar names").pack()

    def select_movie_from_lb(self,name):
        self.movie_name.set("Currently selected: "+name)
        for movie in self.rs.movie_instances:
            if movie.name==name:
                self.movie_id = movie.id
                return
        

    def dbclick(self, event):
        item = self.listbox.get('active')  #get clicked item
        self.dbclick_cmds[item]()   # run associated command

    def dbclick1(self, event):
        item = self.listbox.get('active')  #get clicked item
        self.dbclick_cmds1[item]()   # run associated command 

    def dbclick_cmd1(self,i,j):
        i=str('{:.0f}'.format(i*100))
        self.amount_recomended.set('Percentage Recommended: '+i + '%')
        self.movie_recomended.set('Currently Selected: ' +j)
        try:
            self.rate_this_movie_button.pack_forget()
        except:
            pass
        self.rate_this_movie_button = tk.Button(self, text = "Rate this movie",command = lambda:self.select_movie_from_lb(j))
        self.rate_this_movie_button.pack()
                                                
        
    def recommend(self):
        
        self.dbclick_cmds1 = {}
        self.dbclick_cmds1['Double click a Movie name for the percentage recommended'] = lambda: None
        self.dbclick_cmds1[''] = lambda: None
        try:
            self.listbox.pack_forget()
            self.scrollbar.pack_forget()
            self.movie_recomended_label.pack_forget()
            self.amount_recomended_label.pack_forget()
        except:
            pass
        self.listbox = tk.Listbox(self)
        self.listbox.config(width=50)
        self.listbox.insert('end', 'Double click a Movie name for the percentage recommended')
        self.listbox.insert('end', '')
        self.listbox.pack()
        generated = self.rs.generate_recommendations(self.current_user, self.NUM_OF_RECOMMENDATIONS)

        
        self.group = tk.LabelFrame(self, text="Recommendations", padx=5, pady=5)
        self.group.pack(padx=10, pady=10)
        self.amount_recomended = tk.StringVar()
        self.amount_recomended.set('Percentage Recommended: ')
        self.movie_recomended = tk.StringVar()
        self.movie_recomended_label = tk.Label(self, textvariable=self.movie_recomended)
        self.movie_recomended_label.pack()
    
        
        try:
            self.amount_recomended_label.pack_forget()
        except:
            pass
        self.amount_recomended_label = tk.Label(self, textvariable=self.amount_recomended)
        self.amount_recomended_label.pack()


        for rec in generated:
            self.listbox.insert('end', rec[0])
            self.dbclick_cmds1[rec[0]] = lambda i=rec[1], j=rec[0]:self.dbclick_cmd1(i,j)


        self.listbox.bind('<Double-1>', self.dbclick1)
        self.movie_name.set("Currently selected: ")

    

if __name__ == "__main__":
    app = App()
    app.mainloop()
