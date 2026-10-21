class VectorClock:
    """Vector Clock untuk mengurutkan event pada sistem terdistribusi."""

    def __init__(self, num_processes, process_id):
        self.clocks = [0] * num_processes  
        self.process_id = process_id       

    def increment(self):
        """Menambah clock lokal (event lokal)."""
        self.clocks[self.process_id] += 1

    def send_message(self):
        """Menaikkan clock lokal lalu mengembalikan salinan vektor untuk dikirim."""
        self.increment()
        return list(self.clocks)

    def receive_message(self, received_clocks):
        """Menggabungkan vektor yang diterima (nilai maksimum), lalu menaikkan clock lokal."""
        for i in range(len(self.clocks)):
            self.clocks[i] = max(self.clocks[i], received_clocks[i])
        self.increment()

    def __str__(self):
        return f"P{self.process_id}: {self.clocks}"

    def happens_before(self, other_vector_clock):
        """True jika vektor ini terjadi sebelum vektor lain."""
        if self.clocks == other_vector_clock.clocks:
            return False
        all_le = True
        any_lt = False
        for i in range(len(self.clocks)):
            if self.clocks[i] > other_vector_clock.clocks[i]:
                return False
            if self.clocks[i] < other_vector_clock.clocks[i]:
                any_lt = True
        return all_le and any_lt

    def is_concurrent(self, other_vector_clock):
        """True jika kedua vektor tidak saling mendahului."""
        return not (self.happens_before(other_vector_clock) or
                    other_vector_clock.happens_before(self))