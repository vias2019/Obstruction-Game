import sys
import Solver

if __name__=="__main__":
    
    
    userInput = input("User Input (1 or 2 and MM or AB): ")
    
    turn = userInput[0]
    alg = userInput[2] + userInput[3]
    Solver.file = open("Readme.txt","a")
    
    Solver.run_the_program(turn, alg)    

    Solver.file.close()  
    

