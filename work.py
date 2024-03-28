class BankerAlgorithm:
    def __init__(self, allocation, max_demand, available):
        self.allocation = allocation
        self.max_demand = max_demand
        self.available = available
        self.processes = len(allocation)
        self.resources = len(available)

    def is_safe_state(self):
        work = self.available[:]
        finish = [False] * self.processes
        safe_sequence = []

        while True:
            safe = False
            for i in range(self.processes):
                if not finish[i] and all(work[j] >= self.max_demand[i][j] - self.allocation[i][j] for j in range(self.resources)):
                    work = [work[k] + self.allocation[i][k] for k in range(self.resources)]
                    finish[i] = True
                    safe_sequence.append(i)
                    safe = True
                    break
            if not safe:
                break

        return all(finish), safe_sequence

    def request_resources(self, process_id, request):
        for i in range(self.resources):
            if request[i] > self.max_demand[process_id][i] - self.allocation[process_id][i]:
                return False

        if all(self.available[i] >= request[i] for i in range(self.resources)):
            for i in range(self.resources):
                self.available[i] -= request[i]
                self.allocation[process_id][i] += request[i]
            safe, sequence = self.is_safe_state()
            if safe:
                return True
            else:
                # Rollback changes
                for i in range(self.resources):
                    self.available[i] += request[i]
                    self.allocation[process_id][i] -= request[i]
                return False
        else:
            return False


class DeadlockDetection:
    def __init__(self, allocation, request):
        self.allocation = allocation
        self.request = request
        self.processes = len(allocation)
        self.resources = len(allocation[0])

    def is_deadlocked(self):
        work = [sum(self.allocation[i][j] for i in range(self.processes)) for j in range(self.resources)]
        finish = [False] * self.processes

        while True:
            found = False
            for i in range(self.processes):
                if not finish[i] and all(work[j] >= self.request[i][j] for j in range(self.resources)):
                    for j in range(self.resources):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    found = True
                    break
            if not found:
                break

        return any(not x for x in finish)


if __name__ == "__main__":
    # Example usage of Banker's algorithm
    print("Enter the number of processes:")
    processes = int(input())
    print("Enter the number of resources:")
    resources = int(input())

    allocation = []
    max_demand = []
    print("Enter allocation matrix:")
    for i in range(processes):
        allocation.append(list(map(int, input().split())))
    print("Enter max demand matrix:")
    for i in range(processes):
        max_demand.append(list(map(int, input().split())))
    print("Enter available resources:")
    available = list(map(int, input().split()))

    banker = BankerAlgorithm(allocation, max_demand, available)
    safe, sequence = banker.is_safe_state()
    if safe:
        print("Safe state")
        print("Safe sequence:", sequence)
    else:
        print("Unsafe state")

    # Example usage of deadlock detection algorithm
    print("Enter allocation matrix:")
    allocation = []
    for i in range(processes):
        allocation.append(list(map(int, input().split())))
    print("Enter request matrix:")
    request = []
    for i in range(processes):
        request.append(list(map(int, input().split())))

    detection = DeadlockDetection(allocation, request)
    if detection.is_deadlocked():
        print("Deadlock detected")
    else:
        print("No deadlock detected")
