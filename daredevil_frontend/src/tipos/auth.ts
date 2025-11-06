'use server';
import { type User } from './user';
import { v4 as uuidv4 } from 'uuid';

const DELAY = 1000;

export async function signIn(): Promise<User> {
  return new Promise((resolve) =>
    setTimeout(
      () =>
        resolve({
          id: uuidv4(),
          clientId: 'some-client-id',
          email: 'adam@example.com',
          gitId: 'some-git-id',
          token: 'some-token',
          username: 'Adam',
        }),
      DELAY,
    ),
  );
}

export async function signOut(): Promise<void> {
  return new Promise((resolve) =>
    setTimeout(() => resolve(undefined), DELAY),
  );
}
