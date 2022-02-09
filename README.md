# THE WEB OF INSTAGRAM FOLLOWERS
*Visualizing the connection between followers*

---

# TLDR:

Here are the final visualizations:

![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/final/temp.png)
![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/final/temp%202.png)

---

# FULL PROCCESS
**INITIAL IDEA:**

I wanted to create a web of all my followers and all of their followers. In this model, I was planning on using dots to represent each person, and having their position be calculated based on the number of followers they share with everyone else. For example, if there were 5 people that had very similar followers, they would be closer to each other than a group of people with different followers. In doing this, I was hoping to reveal social clusters of people

**DATA COLLECTION:**

My first step was to research a way to get all this data, as the form and extent of this source would dictate how I would visualize this network. After swiftly concluding that Instagram’s API is the worst thing to have ever been invented by human kind, I did a bit of digging and found this [lovely resource]( https://phantombuster.com), which scrapes databases and social networks automatically and returns them in clean CSVs! Specifically this tool was great, as it operated under the limitations of Instagrams pull request limit, so I was able to setup an hourly automation, to retrieve an allowed amount of items, and then run that for about a day to get my full dataset. 

The contents of my ```data``` source are:
>data
>>followerList: 		This is a trimmed version of the data mentioned above. It has 8 of my followers for a total of 8000 users

>>result (1): 		This is the full version of the data, it has around 160 000 users

# ATTEMPT 1:
*and so it begins*

---

The first thing that I did once I had my data was to turn to the good ol ```test.py```. In this file I did the bulk of my initial experiments. First I created a class that would be able to more intuitively store all the connections between these nodes:
>person
>> following
>
>>followers
>
>>position (x, y)

And then, with the use of some handy functions, generated a list of people classes that represented each user I collected!

**VIS 1** 

First, to see what I was working with, I assigned random coordinates to each person, and rendered them. (drawing lines between each followee and their followers). The result, as sort of expected, was just a scribble of lines. This gave way for what would soon become the most epic struggle of all time: drawing each node with a position relative to all other nodes

![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/Screen%20Shot%202022-01-28%20at%209.25.00%20PM.png)

**VIS 2** 

For this second vis, I don’t know. I do not know what I did to produce this graph, I took a weird average of the positions, multiplied by some things here and there, realized that I was reading the excel file wrong, and ultimately came up with this incredibly broken, and useless visualization. (It is in here because it looks really cool *of course :)*)

![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/Screen%20Shot%202022-01-28%20at%209.40.28%20PM.png)

**VIS 3**

On day 3 I decided to really sit down with this system, and try to work out how I could render each node in relation to each other. My initial thought was to simply render the position of a followee (which I will refer to as a child for the rest of this write up), as the average position of all of its followers (which I will call parents). 

To begin working out the logic of this structure, I turned to my notebook and wrote out some of the functions, loops, and calculations I would need to do in order to solve this problem.

![Image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/notes/IMG_61627B5B16A4-1.jpeg)

Once I had this, I typed up the code, and after spending a few hours debugging stack overflows, out of range indexes, and one bug that I never fully understood, I hit build, and got an incredibly underwhelming render. *so underwhelming in fact, that I did not take a screenshot of it* The algorithm more or less returned random looking points, an issue made much worse when connecting the dots with lines. I decided then to get rid of some of the “junk people”, or nodes that did not have any children in common with their parent, since I noticed this was a huge category that wasn’t necessarily contributing to the visualization how I would have liked. So, I created a threshold, so that if a child had less than 0.1 % of the same children as its parent, it would be sent to a random pos in a ring outside the main vis, and would not get a line drawn to it. While this partly worked, it was confusing, and the data was manipulated in such a way that it was hard to make meaningful relationships out of the visualization. And worst of all: **It didn’t look that good**

![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/Screen%20Shot%202022-01-29%20at%206.29.33%20PM.png)

# ATTEMPT 2:
*A not so sudden realization*

After working on this project for about a day straight, and not achieving any tangible progress, I decided to step away from the problem, and come back to it with fresh eyes, and perhaps the aid of a comp sci class. 

Once I was back in the classroom, I asked a peer what his take was, and he suggested that I develop a **distance matrix**, or some matrix that relates each person to each other person in the dataset. So, I developed a function that would turn the original dataset into a matrix containing the % of same followers between each pair of people in the dataset. 
>data
>>matrix: 		the full, very very big matrix

>>matrixSmall: 		A much *much* smaller matrix, that was able to quickly be imported using pandas

With this, and after a quick discussion with Tom, I concluded that the best way to locate everyone’s position would be to assign them all random positions, then slowly iterate through, finding everyone’s new positions via a weighted average with each iteration. The weight for this average was the distance between two people from the matrix, multiplied by their position. 

Unfortunately, while this seemed promising, the computational power required to loop through the height of the matrix, and then for each of those loops, looping through the width of the matrix to compute these averages proved to be far beyond my laptop and the school computers, even when the matrix was trimmed down to 70 x 70. I decided then to refocus my efforts on optimizing my processes, and after an incredible discussion with Dr. Z, I began looking at this problem as not a series of loops, but as a system of matrix calculations, as that was exponentially faster. So I, once again, turned to my notebook to work out the math of calcualting the weighted average described above with only matrix operations:

![Image]( https://github.com/Brian-Masse/Network-Vis/blob/main/exports/notes/IMG_A04043AEF272-1.jpeg )

With this I took to the numpy documentation, and created ```matrix_testing.py``` to test some of my learning. Once I felt confident with the framework.

Once I had this procedure developed, and eventually coded up ( this was a  tremendously  painful task: for some reason, I had to sink a few hours into what felt like trivial bug fixing. There is no value from me sharing this, I just think its crazy how CS can snag you for hours with a minor problem!), I noticed a ***MAJOR FLAW:***

Computing the positions for each iteration with an average of the previous iteration’s positions meant that, after a few thousand loops, all the points would converge into one. This was a fundamental flaw that broke nearly all the work that I had done prior to this, and what’s even better, I discovered it the day before the project was due! Yay :)

#ATTEMP 3:
### *defeat*

I began reassessing the way in which I computed the positions for each person relative to each other. While I could walk through each idea that I tried, I think my frantic, bombshell notes speak for themselves:

![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/notes/IMG_78AF2723957E-1.jpeg)
![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/notes/IMG_0F55EDB87106-1.jpeg)

Eventually, after spending about 2 hours considering how to position these people, I decided to do what was ultimately most productive, and search for a simpler visualization of this dataset.

#ATEMPT 4:
### *Acceptance*

Enter ```final.py```

I decided that if I cannot render the whole network, it would be interesting to render a central person surrounded by every other node in a circle, where the distance from a given person to the center person is proportional to the distance (from the distance matrix), between these two people. I then expanded this so that every person in this circle would run the same function, but with them as the central person. This was a quick and interesting render that led to a few cool visualizations. 

**VIS 1**
Using the very trimmed data, I surrounded myself with all the people from the dataset and nothing else. I am also including the final visualization I made, which displayed the same data, using the full dataset 

![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/final/Screen%20Shot%202022-02-09%20at%202.04.43%20AM.png)
![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/final/Screen%20Shot%202022-02-09%20at%201.10.06%20AM.png)

**VIS 2**
This used the second method, where I am surrounded by every person in the dataset, and they too are surrounded by every person in the dataset. Similar to the previous vis, I have included both renders that use the smaller and larger datasets. 

![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/final/Screen%20Shot%202022-02-09%20at%201.03.11%20AM.png)
![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/final/Screen%20Shot%202022-02-09%20at%202.02.34%20AM.png)

This vis, using the full dataset, and showing the same information as the previous two, is far too zoomed in, but I thought it looked nice, so I kept it :)

![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/Screen%20Shot%202022-02-09%20at%2012.53.21%20AM.png)

#CONCLUSION:

Don’t try this at home.

This was an incredibly long, bug filled process, that did not end up resulting in the visualization that I wanted to create. **HOWEVER** there were many valuable things that I learned / remembered:
1.	Use paper to write down logic. It is easier and faster than coding, and you can come up with, understand, and address edge cases on paper way faster than if they are lost thoughout your code. When I was trying to redesign the positioning system, going first to my notebook saved me hours that I would have spent coding each idea. 

2.	Experiment with iterations of the same idea. All of the cool final visualizations that I produced would not have come if I did not experiment at each stage of the process. Without adopting matrix multiplication, I would not have discovered the flaw with averaging. Without further probing the dataset, I would have never realized the major flaws presented by my second vis. I believe the quality of revision and change was strong throughout this whole project. 

Overall this was a great learning experience, and although I did not produce the visualization I was hoping to, I am incredibly proud of both the amount and quality of work I did to produce this project!

Here are the final visualizations, labels added in post:

![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/final/temp.png)
![image](https://github.com/Brian-Masse/Network-Vis/blob/main/exports/final/temp%202.png)

