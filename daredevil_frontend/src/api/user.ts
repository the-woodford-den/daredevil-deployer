import type { User } from '@data/user';

interface UserResponse {
  user_token: string;
}

export const getUserToken = async (client_id: string): Promise<User> => {
  try {
    const options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ client_id }),
    };

    const response = await fetch(`${import.meta.env.BACKEND_URL}github/create-token`, options);

    if (!response.ok) {
      console.error('Response was not ok!', response.status);
      const data: Error = (await response.json()) as Error;
      throw new Error(`Response was not ok: ${response.status} - ${data.message}`);
    }

    const data: UserResponse = (await response.json()) as UserResponse;
    return data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      console.error('was an error!', error.message);
      throw new Error(`Could not fetch User token due to: ${error.message}`);
    } else {
      console.error('unknown error!', error);
      throw error;
    }
  }
};
