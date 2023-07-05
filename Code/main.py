from gg1 import GG1Queue, PDF

# Example usage:
if __name__ == "__main__":
    queue = GG1Queue(1000, PDF.EXPONENTIAL, PDF.EXPONENTIAL, scale=1.0)
    queue.run_simulation()
    queue.plot_queue_length()
    print(queue.get_queue_stats())