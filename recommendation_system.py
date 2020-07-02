##
# recommendation_system.py
# This is a movie recommendation system that will suggest movies for users
# based on their history of movies liked and disliked

# Version 1.0
import math
import csv
import tkinter

FILE = 'small_data'
#FILE = 'big_data'
LIKED_RATING = 4

class Movie():
    def __init__(self, __id, name,genres):
        self.id = __id
        self.name = name
        self.genres = genres.split('|')
        
class User():
    def __init__(self, __id):
        self.id = __id
        self.__movies_liked = set()
        self.__movies_disliked = set()
        self.__genres_liked = {}
        self.__genres_disliked = {}
        
    def add_movie_liked(self,__id,movies):
        self.__movies_liked.add(__id)
        for movie in movies:
            if movie.id == __id:
                for genre in movie.genres:
                    try:
                        self.__genres_liked[genre] = self.__genres_liked[genre] +1
                    except:
                        self.__genres_liked[genre] = 1
        
    def add_movie_disliked(self,__id,movies):
        self.__movies_disliked.add(__id)
        for movie in movies:
            if movie.id == __id:
                for genre in movie.genres:
                    try:
                        self.__genres_disliked[genre] = self.__genres_disliked[genre] +1
                    except:
                        self.__genres_disliked[genre] = 1


    def get_movies_liked(self):
        return self.__movies_liked
    
    def get_movies_disliked(self):
        return self.__movies_disliked

    def get_genres_liked(self):
        return self.__genres_liked
    
    def get_genres_disliked(self):
        return self.__genres_disliked
 
    def likes(self, movie):
        if movie in self.__movies_liked:
            return True
        return False
    
    def dislikes(self,movie):
        if movie in self.__movies_disliked:
            return True
        return False

    def __gt__(self, other):
        return self.id > other.id
    
    def __lt__(self,other):
        return self.id < other.id

class Rs():
    def __init__(self):
        self.movies, self.movie_instances, self.ratings, self.users,self.genres = self.importdata()

    def importdata(self):
        '''Load CSV files to memory'''
        movies, ratings, users, genres = [],[],[],[]

        u_ids = []
        m_ids = []

        with open(FILE+'/movies.csv', encoding='utf-8') as csv_file:
            line_count = 0
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if line_count == 0:
            #print('Column names are {}'.format(', '.join(row)))# Use pass
                    pass
                else:
                    movies.append(Movie(row[0],row[1],row[2]))
                    for g in row[2].split('|'):
                        if g not in genres:
                            genres.append(g)
                line_count += 1
          
 
                
        with open(FILE+'/ratings.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    #print('Column names are {}'.format(', '.join(row)))# Use pass
                    pass
                else:

                    # Do this with a dictionary
                    # dict = {id:{movie:rating}}
                    if row[0] not in u_ids:
                        users.append(User(row[0]))
                        u_ids.append(row[0])
                        
                    if row[1] not in m_ids:
                        m_ids.append(row[1])
                        
                    for user in users:
                        if user.id == row[0]:
                            if float(row[2]) > LIKED_RATING:
                                user.add_movie_liked(row[1],movies)
                            else:
                                user.add_movie_disliked(row[1],movies)
                        
                    #print('UserId:{}, MovieID:{}, Rating:{}'.format(row[0], row[1], row[2]))
                line_count += 1

        # Do other files


        return m_ids,movies, ratings, users, genres


    def user_movies(self,user):
        """ Return the liked and disliked movie SETS for the given user"""
        for u in self.users:
            if u == user:
                return user.get_movies_liked()|user.get_movies_disliked()
                
    def return_users_liked(self,movie):
        """ Return the set of all users who liked a movie(object)"""
        users_liked = set()
        for u in self.users:
            if u.likes(movie):
                users_liked.add(u)
        return users_liked

    def return_users_disliked(self,movie):
        """ Return the set of all users who disliked a movie(object)"""
        users_disliked = set()
        for u in self.users:
            if u.dislikes(movie):
                users_disliked.add(u)

        return users_disliked

    def find_similar_users(self,CURRENT_USER):
        """ Given a user, compute a list of other users who are similar
    Store the list in a database (in this case a dictionary), along with their similarity indicies
    Return the list of similar users in order of most to least similar"""
        sim_users_set = set()
        sim_users_list = []
        
        ''' Create our similar users set (all users that have rated a movie the user has rated)'''
        u_movies = self.user_movies(CURRENT_USER)
        for m in u_movies:
            t = self.return_users_liked(m)|self.return_users_disliked(m)
            sim_users_set = sim_users_set | t
     
        for u in sim_users_set:
            #simularity index
            if u != CURRENT_USER:
                sim_users_list.append((self.similarity_index(CURRENT_USER, u),u))
        return sorted(sim_users_list, reverse = True)


    def possibility_index(self,CURRENT_USER, movie):
        """
        Given a user(object) and a movie(object)
        Find all users who have rated this movie (obviously not the current one
        Compute the similarity index of each user and use it to
        Generate the possiblity of a user liking a given movie
        """
        ## Finding the sum of the similarity indicies of all users who have LIKED a movie
        # Variable to store the sum of all the similarity indicies of all users who have liked a given movie
        sum_i_l = 0
        # For each user in the set of return_user_liked(movie)
        for u in self.return_users_liked(movie):
            #if u is not current user
            if u != CURRENT_USER:
                # Add the return of the similarity_index(CURRENT_USER,user)to our sum
                sum_i_l += self.similarity_index(CURRENT_USER,u)

        ## Finding the sum of the similarity indicies of all users who have DISLIKED a movie
        # Variable to store the sum of all the similarity indicies of all users who have liked a given movie
        sum_i_dl = 0
        # For each user in the set of return_user_disliked(movie)
        for u in self.return_users_disliked(movie):
            #if u is not current user
            if u != CURRENT_USER:
                # Add the return of the similarity_index(CURRENT_USER,user)to our sum
                sum_i_dl += self.similarity_index(CURRENT_USER,u)

        ##Calculate and return the probability of the user likeing a movie
        ## The possiblilty index is calculated by
                # the sum of all the similarity indicies of all the users who liked the given movie MINUS
                # the sum of all the similarity indicies of all the users who disliked the given movie /
                # the # of users who liked the given movie plus the # of all users who have disliked the movie
        n = sum_i_l - sum_i_dl
        d = len(self.return_users_liked(movie)) + len(self.return_users_disliked(movie))
        return n/d

    def similarity_index(self, CURRENT_USER, user):
        """
        Return the similarity index of two users between -1.0 and 1.0
        Originally known as "Coefficient de communaute" by Paul Jaccard
        """

        U1 = CURRENT_USER
        U2 = user
        #define liked sets of each user to use in formula
        l = U1.get_movies_liked()
        l2 = U2.get_movies_liked()
        #define disliked sets of each user to use formula
        d = U1.get_movies_disliked()
        d2 = U2.get_movies_disliked()

        #calculate similarity index
        similarity_index = (len((l&l2))+len((d&d2))-len((l&d2))-len((l2&d)))/len((l|l2|d|d2))

        U1 = CURRENT_USER
        U2 = user
        #define liked sets of each user to use in formula
        l = U1.get_genres_liked()
        l2 = U2.get_genres_liked()
        d = U1.get_genres_disliked()
        d2 = U2.get_genres_disliked()

        a =0
        b=0
        c=0
        f=0
        e=0
        
        for genre in self.genres:
            try:
                a += l[genre] + l2[genre]
            except:
                pass
            try:
                b += d[genre] + d2[genre]
            except:
                pass
            try:
                c += l[genre] + d2[genre]
            except:
                pass
            try:
                f += d[genre] + l2[genre]
            except:
                pass
          
        e = a+b+c+f
        genre_similarity = (a+b-c-f)/e

        return (similarity_index + genre_similarity) /2



    def set_current_user(self, user_id):
        """ Assign the current user to an instance"""
        CURRENT_USER = ""
        for user in self.users:
            if user.id == user_id:
                CURRENT_USER = user
        return CURRENT_USER

    """ *** Genterating recommendations *** """

    def return_unrated(self,CURRENT_USER):
        """Return a list of all unrated movie ids a given user has not rated """
        # Create a list to store all movie ids of unrated movies
        unrated_movie_ids = []
        # For each user in the list of similar users
        a =set()
        for u in self.find_similar_users(CURRENT_USER):
            #user rated and cu not
            a = a | (self.user_movies(u[1]) - self.user_movies(CURRENT_USER))###################
        for m in a:
            unrated_movie_ids.append(m)
        return unrated_movie_ids

    def unrated_movie_possibilities(self,CURRENT_USER):
        """Store all items the given user has not rated with the possibility index and return the dictionary """

        """Compute possibility of user liking a movie"""
        # Create an empty dictionary
        recommended_movies = {}
        self.min = 1
        self.max = -1
        for movie in self.return_unrated(CURRENT_USER):
            recommended_movies[movie] = self.possibility_index(CURRENT_USER, movie)# Tuples
            if recommended_movies[movie] > self.max:
                self.max = recommended_movies[movie]
            if recommended_movies[movie] < self.min:
                self.min = recommended_movies[movie]
                
            
        return recommended_movies

    def generate_recommendations(self,CURRENT_USER, num_recommendations):
        recommended_movies = self.unrated_movie_possibilities(CURRENT_USER)
        counter = 0
        l = []
        for key,value in sorted(recommended_movies.items(), key = lambda x:x[1], reverse = True):
            if counter<num_recommendations:
                for movie in self.movie_instances:
                    if key == movie.id:
                        l.append((movie.name, self.normalise(value)))
                counter+=1
            else:
                return l

    def normalise(self, x):
        normalized = (x/1.1-self.min/1.1)/(self.max-self.min/1.1)
        return normalized
            
if __name__ == "__main__":
    print("Wrong one dumbass")
