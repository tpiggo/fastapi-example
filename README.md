# FastApi Playground

Welcome to my fastapi playground where I am learning to familiarize myself with FastApi again after sometime 
not using it. Back during my previous job, I used FastApi some with projects and got a good grasp on the framework.
However it has been some time since then, so I have decided it would be a good idea to practice rebuilding some 
apps using the framework.

The project is split into two different parts:
1. The MainApi int he mainapi folder. Here is where most of the work will be done
2. OAuth Server: This is a simple auth server I built in order to have some idea behind security and better leverage the dependency injection. Moreover, in my old job, no one knew how to properly make the dependency injection work for this kind of problem therefore, security took a back seat. Here we are not going to overlook the concept but will only implement a simple version

Both applications are meant to be built into containers to be run properly and there will be a docker-compose file in the main
directory of the project such that it will be simple to spin up the whole application 

Happy reading :)