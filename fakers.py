from faker import Faker
import random

fake = Faker()

def generate_synthetic_data(num_samples):
    data = []
    for _ in range(num_samples):
        # Generate random text samples
        text_type = random.choice(['sentence', 'paragraph', 'name', 'address'])
        
        if text_type == 'sentence':
            data.append(fake.sentence())
        elif text_type == 'paragraph':
            data.append(fake.paragraph())
        elif text_type == 'name':
            data.append(fake.name())
        elif text_type == 'address':
            data.append(fake.address())
    
    return data

# Generate 1000 synthetic text samples
synthetic_data = generate_synthetic_data(1000)

# Save the data to a file
with open('synthetic_dataset.txt', 'w') as file:
    for text in synthetic_data:
        file.write(text + '\n')

