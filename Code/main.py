from gg1 import GG1Queue, PDF

# Example usage:
if __name__ == "__main__":
    queue = GG1Queue(1000, PDF.EXPONENTIAL, PDF.EXPONENTIAL, {'scale':1.2}, {'scale':1.2})
    queue.run_simulation()
    queue.plot_queue_length()
    print(queue.get_queue_stats())

    SERVICE_EXPONENTIAL_KWARGS = {'scale': 1.2}
    ARRIVAL_EXPONENTIAL_KWARGS = {'scale': 1.5}

    SERVICE_NORMAL_KWARGS = {'loc': 0, 'scale': 1.0}
    ARRIVAL_NORMAL_KWARGS = {'loc': 0.5, 'scale': 1.5}

    SERVICE_HAWKES_KWARGS = {'mu': 1.0, 'alpha': 1.5, 'beta': 0.8}
    ARRIVAL_HAWKES_KWARGS = {'mu': 1.2, 'alpha': 1.8, 'beta': 1.0}

    SERVICE_UNIFORM_KWARGS = {'low': 0.5, 'high': 1.5}
    ARRIVAL_UNIFORM_KWARGS = {'low': 0, 'high': 0.5}

    queue = GG1Queue(1000, PDF.EXPONENTIAL, PDF.HAWKES, SERVICE_EXPONENTIAL_KWARGS, ARRIVAL_HAWKES_KWARGS)
    queue.run_simulation()
    queue.plot_queue_length()
    print(queue.get_queue_stats())
