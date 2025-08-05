import React, { useEffect, useState } from 'react';
import api from '../api.js';
import AddFruitForm from './AddFruitForm';

interface Fruit {
  id: number; // Assuming each fruit has a unique ID
  name: string;
}

const FruitList: React.FC = () => {
  const [fruits, setFruits] = useState<Fruit[]>([]);

  const fetchFruits = async () => {
    try {
      const response = await api.get<{ fruits: Fruit[] }>('/fruits');
      setFruits(response.data.fruits);
    } catch (error) {
      console.error('Error fetching fruits', error);
    }
  };

  const addFruit = async (fruitName: string) => {
    try {
      await api.post('/fruits', { name: fruitName });
      fetchFruits(); // Refresh the list after adding a fruit
    } catch (error) {
      console.error('Error adding fruit', error);
    }
  };

  useEffect(() => {
    fetchFruits();
  }, []);

  return (
    <div>
      <h2>Fruits List</h2>
      <ul>
        {fruits.map((fruit) => (
          <li key={fruit.id}>{fruit.name}</li>
        ))}
      </ul>
      <AddFruitForm addFruit={addFruit} />
    </div>
  );
};

export default FruitList;