import { useEffect, useState } from 'react';
import { api } from '../../api/client';
import { Plant } from '../../types/plant';

export function PlantsPage() {
  const [plants, setPlants] = useState<Plant[]>([]);
  useEffect(() => {
    void api.get('/plants').then((r) => setPlants(r.data)).catch(() => setPlants([]));
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-semibold">My plants</h1>
      <ul className="mt-4 space-y-2">
        {plants.map((plant) => (
          <li className="rounded border p-3" key={plant.id}>{plant.name}</li>
        ))}
      </ul>
    </div>
  );
}
