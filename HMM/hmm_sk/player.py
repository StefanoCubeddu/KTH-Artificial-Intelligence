#!/usr/bin/env python3

from player_controller_hmm import PlayerControllerHMMAbstract
import random
from constants import *
import math
import numpy as np



def first_mult(P,init):
    res=[]
    for x in range(len(P)):
       # print(type(P),type(init),type(P[x]),type(init[x]))
        res.append(P[x]*init[x])
    return res


def mult(X,Y):
   result=[]
   for y in range(len(Y[0])):
      value=0
      for x in range(len(X)):
        value+=X[x]*Y[x][y]
      result.append(value)
   return result

def get_obs_prob(B):
    mat=[]
    for j in range(len(B[0])):
        line=[]
        for i in range(len(B)):
            line.append(B[i][j])
        mat.append(line)
    return mat


def forward(observations,A,B,pi):
    i=0
    obs_prob=get_obs_prob(B)
    alpha=[]
    alpha_store=[]
    while(i<len(observations)):
        if(i==0):
            alpha=first_mult(pi,obs_prob[int(observations[i])])
            alpha_store.append(alpha)
        else:  
            alpha=(first_mult(mult(alpha,A),obs_prob[int(observations[i])]))
            alpha_store.append(alpha)
        i+=1
    return sum(alpha)



def get_alpha(pi,A,B,observations):
    t=0
    alpha_store=[]
    temp=[]
    c0=0
    ct=[]
    cu=0
    val=0
    while(t<len(observations)):
       temp=[] 
       if(t==0):
          for i in range(len(A)):
                val=pi[i]*B[i][int(observations[t])]
                temp.append(val)
                c0+=val
          c0=1/c0
          ct.append(c0)
          for i in range(len(A)):
            temp[i]=c0*temp[i]
          alpha_store.append(temp)
       else:
            cu=0
            for i in range(len(A)):
                val=0
                for j in range(len(A)):
                    val+=alpha_store[t-1][j]*A[j][i]
                val=val*B[i][int(observations[t])]
                temp.append(val)
                cu+=val
            cu=1/cu
            ct.append(cu)
            for i in range(len(A)):
                temp[i]=cu*temp[i]
            alpha_store.append(temp)
       t+=1
    return alpha_store,ct


def get_beta(A,B,observations,ct):
    t=len(observations)-1
    count=0
    beta=[]
    while(t>=0):
        temp=[]
        if(t==len(observations)-1):
            for i in range(len(A)):
                temp.append(ct[t])
            count+=1
            t-=1
            beta.append(temp)
        else:
            for i in range(len(A)):
                val=0
                for j in range(len(A)):
                    val=val+A[i][j]*B[j][int(observations[t+1])]*beta[count-1][j]
                val=val*ct[t]
                temp.append(val)
            beta.append(temp)
            count+=1
            t-=1
    return beta


def get_gamma(beta,alpha,observations,A,B):
    t=0
    gamma=[]
    gamma_sum=[]
    while(t<(len(observations)-1)):
        temp=[]
        temp_sum=[]
        for i in range(len(A)):
            temp2=[]
            for j in range(len(A)):
                val=0
                val=alpha[t][i]*A[i][j]*B[j][int(observations[t+1])]*beta[t+1][j]
                temp2.append(val)
            temp.append(temp2)
            temp_sum.append(sum(temp2))
        gamma.append(temp)
        gamma_sum.append(temp_sum)
        t+=1
    
    temp=[]
    for i in range(len(A)):
        temp.append(alpha[len(observations)-1][i])
    gamma_sum.append(temp)
    
    return gamma,gamma_sum

def reastimate(A,B,gamma,gamma_sum,observations):
    pi=[]
    t=0
    for i in range(len(A)):
        pi.append(gamma_sum[t][i])

    for i in range(len(A)):
        denom=0
        for t in range(len(observations)-1):
            denom+=gamma_sum[t][i]
        for j in range(len(A)):
            numer=0
            for t in range(len(observations)-1):
                numer+=gamma[t][i][j]
            A[i][j]=numer/denom

    for i in range(len(A)):
        denom=0
        for t in range(len(observations)-1):
            denom+=gamma_sum[t][i]
        for j in range(len(B[0])):
            numer=0
            for t in range(len(observations)-1):
                if(int(observations[t])==j):
                    numer+=gamma_sum[t][i]
            B[i][j]=numer/denom
    return A,B,pi



def get_AB(A,B,pi,observations):
    max_iters=100
    iters=0
    oldLogProb=float('-inf')

    flag=True
    while(flag):

        alpha,c=get_alpha(pi,A,B,observations)
        beta=get_beta(A,B,observations,c)
        beta.reverse()
        gamma,gamma_sum=get_gamma(beta,alpha,observations,A,B)
        A,B,pi=reastimate(A,B,gamma,gamma_sum,observations)
        logProb=0
        iters+=1
        for i in range(len(observations)):
            logProb+=math.log(c[i])
        logProb=-logProb
        iters+=1
        if(iters<max_iters and logProb>oldLogProb):
            oldLogProb=logProb
        else:
            flag=False
    return A,B,pi





def generate_matrix(size):
    M = [(1 / size) + np.random.rand() / 1000 for _ in range(size)]
    s = sum(M)
    return [m / s for m in M]








class Model:
    def __init__(self, species, emissions):
        self.PI = [generate_matrix(species)]
        self.PI=self.PI[0]
        self.A = [generate_matrix(species) for _ in range(species)]
        self.B = [generate_matrix(emissions) for _ in range(species)]

    def set_A(self, A):
        self.A = A

    def set_B(self, B):
        self.B = B

    def set_PI(self, PI):
        self.PI = PI


    


class PlayerControllerHMM(PlayerControllerHMMAbstract):

    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        self.model_fish = [Model(1,N_EMISSIONS) for _ in range(N_SPECIES)]

        self.fish = [(i, []) for i in range(N_FISH)]


    def update(self,id):
        A=self.model_fish[id].A
        B=self.model_fish[id].B
        pi=self.model_fish[id].PI
        A,B,pi=get_AB(A,B,pi,self.obs)
        A=self.model_fish[id].set_A(A)
        B=self.model_fish[id].set_B(B)
        pi=self.model_fish[id].set_PI(pi)


    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """
    
        # This code would make a random guess on each step:
        # return (step % N_FISH, random.randint(0, N_SPECIES - 1))
        for i in range(len(self.fish)):
            self.fish[i][1].append(observations[i])


        if step < 95:  
            return None
        else:
            fish_id, obs = self.fish.pop()
            print(obs)
            fish_type = 0
            max = 0
            for model, j in zip(self.model_fish, range(N_SPECIES)):
                m = forward(obs, model.A,model.B,model.PI)
                if m > max:
                    max = m
                    fish_type = j
            self.obs = obs
            return fish_id, fish_type

    def reveal(self, correct, fish_id, true_type):
        """
        This methods gets called whenever a guess was made.
        It informs the player about the guess result
        and reveals the correct type of that fish.
        :param correct: tells if the guess was correct
        :param fish_id: fish's index
        :param true_type: the correct type of the fish
        :return:
        """
        if(not correct):
            self.update(true_type)


