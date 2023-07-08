'''
Filename: \queue_sim\gg1.py
Path: \queue_sim
Created Date: Wednesday, June 28th 2023, 12:12:34 pm
Author: pranofgit (Pranjal Pandey)
'''


import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from enum import Enum


class PDF(Enum):
    """to keep track of pdf names for the queue (service and arrival)"""
    NORMAL = 1
    EXPONENTIAL = 2
    WEIBULL = 3
    UNIFORM = 4
    HAWKES = 5
    CUSTOM = 6

class GG1Queue:
    """
    General/General/1/k Queue simulation class. 
    
    It supports normal, exponential, Weibull, and uniform pdfs.

    kwargs : dict
        Additional arguments for the pdfs. These can be:
            For NORMAL: loc (mean), scale (standard deviation)
            For EXPONENTIAL: scale (mean or 1/lambda)
            For WEIBULL: a (shape)
            For UNIFORM: low (lower boundary), high (upper boundary)
            For HAWKES: mu (mean), alpha (excitation), beta (decay) [keep alpha less than beta]
    """
    #TODO 1: verify hawkes
    # TODO 2: mm1 unit test

    def __init__(self, tot_arrivals:int, service_pdf:PDF, arrival_pdf:PDF, service_kwargs={}, arrival_kwargs={}):
        self.queue = deque()
        self.tot_arrivals = int(tot_arrivals)
        self.service_pdf = service_pdf
        self.arrival_pdf = arrival_pdf
        self.service_kwargs = service_kwargs #Additional arguments for the service pdf.
        self.arrival_kwargs = arrival_kwargs #Additional arguments for the arrival pdf.
        self.time_series = [] # stores tuple (time, queue_length) to track the queue length over time.
        self.wait_time = [] # when_serviced - when_arrived
        # saving previous values for non iid process (like hawkes)
        self.generated_arrivals = []
        self.generated_services = []
        # initialize the next arrival and service time
        self.next_arrival_time = self._get_arrival_time()
        self.next_service_time = self.next_arrival_time + self._get_service_time()
       
        
    def _simulate_hawkes_process(self, mu, alpha, beta, num_events):
        current_time = 0
        event_times = []  # list to store event times
        while len(event_times) < num_events:
            thinning_rate = mu + alpha / beta * sum(np.exp(-beta * (current_time - np.array(event_times))))
            inter_event_time = np.random.exponential(1 / thinning_rate) # expo var
            current_time += inter_event_time
            uni_var = np.random.rand() # for thinning
            actual_rate = mu + alpha * sum(np.exp(-beta * (current_time - np.array(event_times))))
            if uni_var <= actual_rate / thinning_rate:
                event_times.append(current_time)
        return event_times

    
    def _get_hawkes_time(self, kind, **kwargs):
        if kind == 'arrival':
            if not self.generated_arrivals:
                self.generated_arrivals = self._simulate_hawkes_process(**kwargs, num_events=self.tot_arrivals)
            return self.generated_arrivals.pop(0)
        elif kind == 'service':
            if not self.generated_services:
                self.generated_services = self._simulate_hawkes_process(**kwargs, num_events=self.tot_arrivals)
            return self.generated_services.pop(0)


    def _get_custom_time(self, kind, **kwargs):
        """This is a placeholder. In the child class can define
          your own custom time distribution for arrival and service"""
        if kind == 'service':
            return np.random.normal(**kwargs)
        elif kind == 'arrival':
            return np.random.normal(**kwargs)

    def _get_service_time(self):
        if self.service_pdf == PDF.NORMAL:
            return np.random.normal(**self.service_kwargs)
        elif self.service_pdf == PDF.EXPONENTIAL:
            return np.random.exponential(**self.service_kwargs)
        elif self.service_pdf == PDF.WEIBULL:
            return np.random.weibull(**self.service_kwargs)
        elif self.service_pdf == PDF.UNIFORM:
            return np.random.uniform(**self.service_kwargs)
        elif self.service_pdf == PDF.HAWKES:
            return self._get_hawkes_time('service',**self.service_kwargs)
        elif self.service_pdf == PDF.CUSTOM:
            return self._get_custom_time('service',**self.service_kwargs)
        else:
            raise ValueError("Invalid service_pdf")

    def _get_arrival_time(self):
        if self.arrival_pdf == PDF.NORMAL:
            return np.random.normal(**self.arrival_kwargs)
        elif self.arrival_pdf == PDF.EXPONENTIAL:
            return np.random.exponential(**self.arrival_kwargs)
        elif self.arrival_pdf == PDF.WEIBULL:
            return np.random.weibull(**self.arrival_kwargs)
        elif self.arrival_pdf == PDF.UNIFORM:
            return np.random.uniform(**self.arrival_kwargs)
        elif self.arrival_pdf == PDF.HAWKES:
            return self._get_hawkes_time('arrival',**self.arrival_kwargs)
        elif self.arrival_pdf == PDF.CUSTOM:
            return self._get_custom_time('arrival',**self.arrival_kwargs)
        else:
            raise ValueError("Invalid arrival_pdf")

    def run_simulation(self):
        """run simulation"""
        left_to_arrive = self.tot_arrivals
        serviced = 0
        while self.tot_arrivals > serviced:
            #arrivals
            while left_to_arrive > 0 and self.next_arrival_time < self.next_service_time:
                self.queue.append(self.next_arrival_time)
                self.time_series.append((self.next_arrival_time, len(self.queue)))
                self.next_arrival_time += self._get_arrival_time()
                left_to_arrive -= 1
            #service
            arrival_time_of_served = self.queue.popleft()
            self.time_series.append((self.next_service_time, len(self.queue)))
            self.wait_time.append(self.next_service_time - arrival_time_of_served)
            serviced += 1
            if len(self.queue) > 0:
                self.next_service_time += self._get_service_time()
            else:
                self.next_service_time = self.next_arrival_time + self._get_service_time()
        message = "run complete"
        return message


    def plot_queue_length(self):
        """plot quelength with time"""
        plt.figure(figsize=(10, 6))
        times, queue_lengths = zip(*self.time_series) # split time and queue length into two lists
        plt.plot(times, queue_lengths, 'b-')
        plt.xlabel('Time')
        plt.ylabel('Queue Length')
        plt.title('Queue length with time')
        plt.grid(True)
        plt.show()

    def get_queue_stats(self):
        """get queue stats"""
        # TODO 4: average queue length (steady state reaches? point after which wait time stops increasing?)
        _, queue_lengths = zip(*self.time_series)
        max_queue_len = max(queue_lengths)
        avg_wait_time = np.mean(self.wait_time)
        return max_queue_len, avg_wait_time
    

        