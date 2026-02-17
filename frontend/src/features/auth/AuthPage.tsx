import { FormEvent, useState } from 'react';
import { api } from '../../api/client';

export function AuthPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    const response = await api.post('/auth/login', { email, password });
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('refresh_token', response.data.refresh_token);
  };

  return (
    <form className="max-w-md space-y-3" onSubmit={submit}>
      <input className="w-full rounded border p-2" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input className="w-full rounded border p-2" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button className="rounded bg-green-600 px-4 py-2 text-white">Login</button>
    </form>
  );
}
