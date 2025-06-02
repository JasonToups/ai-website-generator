import React, { useState } from 'react';

interface ShoppingList {
  id: number;
  name: string;
  items: string[];
}

const Lists: React.FC = () => {
  const [lists, setLists] = useState<ShoppingList[]>([
    { id: 1, name: 'Groceries', items: ['Milk', 'Bread', 'Eggs'] },
    { id: 2, name: 'Hardware Store', items: ['Screws', 'Hammer', 'Nails'] },
  ]);

  const [newListName, setNewListName] = useState('');

  const addNewList = () => {
    if (newListName.trim()) {
      setLists([...lists, { id: Date.now(), name: newListName, items: [] }]);
      setNewListName('');
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Your Shopping Lists</h2>
      <div className="mb-4">
        <input
          type="text"
          value={newListName}
          onChange={(e) => setNewListName(e.target.value)}
          className="border border-gray-300 rounded-md py-2 px-3 mr-2"
          placeholder="New list name"
        />
        <button
          onClick={addNewList}
          className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-300"
        >
          Add New List
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {lists.map((list) => (
          <div key={list.id} className="bg-white shadow-md rounded-lg p-4">
            <h3 className="text-xl font-bold mb-2">{list.name}</h3>
            <ul className="list-disc list-inside">
              {list.items.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Lists;