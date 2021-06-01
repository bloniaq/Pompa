# Pompa
The application is build as a thesis, and works as a help in designing sewage pumping station. 
Basically this is recreation of some early 90s application, which can't be ran on 64-bit OS. 

Application purpose is to get conditions of designed sewage pump station and
* calculate the number of pumps and ordinates to turn on subsequent pumpsets based on the preset shutdown ordinate in checking mode
* calculate the number of pumps, ordinates to turn on subsequent pumpsets, and the most favourable ordinate to shutdown in optimalistaion mode.

After building first working prototype - it was decided to recreate whole project from scratch, due to some mistakes made in architecture. New version is build in TDD workflow, which greatly helps to keep code clean.

At present stage, the main subject of development is model. There is a view section which remains from previous version of project. User interface wass build using pygubu designer https://github.com/alejandroautalan/pygubu Future plans of usage py2exe library probably won't let use this UI builder dependence, so probably UI will be rebuild in plain tkinter but in present shape.

The default branch is now dev.

This project helps me taking the first steps in git usage, also it is my first bigger project, so there are many refactors, commits, changing syntax, etc, because I'm learning much while developing.
