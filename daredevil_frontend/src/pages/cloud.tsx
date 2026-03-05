import { useRef, type FormEvent } from 'react';
import { CreateGitAppForm, CreateGitInstallationForm } from '@/components';
import { Outlet, redirect, useLoaderData } from "react-router";
import {
  Box,
  Flex,
  GridItem,
  Heading,
  Mark,
  HStack,
  Center,
  Text,
} from '@chakra-ui/react';
import type { App, ErrorState, Installation } from '@/tipos';
import { appStore, installationStore, userStore, errorStore } from "@/state";
import { Form } from 'react-router';
import { createApp, createInstallation, getApp, getInstall, getCurrentUser } from '@/api';
import underUrl from '~/underline.svg';


export async function clientLoader() {
  try {
    const userResult = await getCurrentUser();
    const user = await userResult.match(
      (user) => user,
      () => null,
    );

    if (!user) {
      throw redirect("/login");
    }

    if (!userStore.getState().username) {
      await userStore.getState().handleSignIn(user);
    }

    const username = user.username;
    const title = username
      ? `${username.charAt(0).toUpperCase()}${username.slice(1)}'s Cloud Console`
      : 'Cloud Console';

    let app = appStore.getState();
    if (!app.name) {
      const result = await getApp();
      result.match(
        (fetchedApp: App) => { appStore.getState().updateApp(fetchedApp); },
        (err: ErrorState) => { errorStore.getState().setError(err); },
      );
    }

    let installation = installationStore.getState();
    if (!installation.appSlug) {
      const result = await getInstall();
      result.match(
        (install: Installation) => { installationStore.getState().updateInstallation(install); },
        (err: ErrorState) => { errorStore.getState().setError(err); },
      );
    }

    return {
      app: appStore.getState(),
      installation: installationStore.getState(),
      title,
      footer: 'Just Keep Showing Up & Life Will Reward You',
    };
  } catch (err) {
    // Let redirect responses from React Router pass through
    if (err instanceof Response) throw err;
    console.error('[cloud clientLoader] unexpected error:', err);
    throw redirect("/login");
  }
}
clientLoader.hydrate = true;

export default function Cloud() {
  let data = useLoaderData();
  const formRef = useRef<HTMLFormElement>(null);
  const appCreate = appStore(
    (state) => state.createApp,
  );
  const installationCreate = installationStore(
    (state) => state.createInstallation,
  );

  const handleGitApp = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!formRef.current) {
      return;
    }
    const user = userStore.getState();
    if (!user.cookie) {
      console.log(user);
      throw redirect("/login");
    }

    const clientId = data.get("clientId") as string;
    const result = await createApp(user.cookie, clientId);
    result.match(
      (app: App) => {
        appCreate(app);
      },
      (err: ErrorState) => {
        errorStore.getState().setError(err);
      });
    console.log(result);
    formRef.current?.reset();
  };

  const handleGitInstallation = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!formRef.current) {
      return;
    }
    const user = userStore.getState();
    if (!user.cookie) {
      console.log(user);
      throw redirect("/login");
    }

    const username = data.get("username") as string;
    const result = await createInstallation();
    result.match(
      (install: Installation) => {
        installationCreate(install);
      },
      (err: ErrorState) => {
        errorStore.getState().setError(err);
      });
    console.log(result);
    formRef.current?.reset();
  };


  return (
    <>
      <GridItem alignItems="start" colSpan={3}>
        <Center mb="6" pb="6">
          <HStack>
            <Box>
              <Mark
                key={`${data.name}1`}
                css={{
                  fontStyle: 'italic',
                  color: "purple.500",
                  position: "relative",
                }}
              >
                <Heading textStyle="2xl" className="t-font">{data.title}</Heading>
                <img
                  style={{ position: "absolute", left: 0 }}
                  src={underUrl}
                  loading="lazy"
                  alt="line"
                />
              </Mark>
            </Box>
          </HStack>
        </Center>
        <Outlet />
        <Center mt="6" pt="6">
          <Heading textStyle="2xl" className="t-font">{data.footer}</Heading>
        </Center>
      </GridItem>
      <GridItem pt="6" pb="8">
        <Flex
          w="full"
          justify="left"
        >
          <Box
            background="black"
            p="2rem"
            color="white"
            w="65%"
          >
            {data.app.name ? (
              <div>
                <Text textStyle="md">{`App Name: ${data.app.name}`}</Text>
                <Text textStyle="md">{`App ID: ${data.app.id}`}</Text>
                <Text textStyle="md">{`Client ID: ${data.app.gitId}`}</Text>
              </div>
            ) : (
              <Form method="post" ref={formRef} onSubmit={async (e) => { await handleGitApp(e) }}>
                <CreateGitAppForm />
              </Form>
            )}
          </Box>
        </Flex>
      </GridItem>
      <GridItem pt="6" pb="8">
        <Flex
          w="full"
          justify="left"
        >
          <Box
            background="black"
            p="2rem"
            color="white"
            w="65%"
          >
            {data.installation.name ? (
              <div>
                <Text textStyle="md">{`App Name: ${data.installation.appSlug}`}</Text>
                <Text textStyle="md">{`App ID: ${data.installaton.id}`}</Text>
                <Text textStyle="md">{`Git ID: ${data.installation.gitId}`}</Text>
              </div>
            ) : (
              <Form method="post" ref={formRef} onSubmit={async (e) => { await handleGitInstallation(e) }}>
                <CreateGitInstallationForm />
              </Form>
            )}
          </Box>
        </Flex>
      </GridItem>
    </>
  );
}

