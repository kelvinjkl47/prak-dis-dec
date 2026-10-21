from vector_clock import VectorClock

a = VectorClock(num_processes=2, process_id=0)
b = VectorClock(num_processes=2, process_id=1)

a.increment()   
b.increment()  
print("Sebelum ada pesan:")
print(a)
print(b)
print("A concurrent dengan B:", a.is_concurrent(b))

pesan = a.send_message()
b.receive_message(pesan)
print("\nSetelah P0 mengirim pesan ke P1:")
print(a)
print(b)
print("A happens before B:", a.happens_before(b))
print("B happens before A:", b.happens_before(a))
print("A concurrent dengan B:", a.is_concurrent(b))