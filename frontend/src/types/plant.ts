export interface Plant {
  id: number;
  name: string;
  latin_name?: string;
  water_interval_days: number;
  next_watering_date?: string;
}
