import { useRef, type FormEvent } from 'react';
import { CreateAppForm, CreateInstallationForm } from '@/components';
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
import { createApp, createInstallation, getApp, getInstall } from '@/api';
import underUrl from '~/underline.svg';


export async function clientLoader() {
  const user = userStore.getState();
  if (!user.username) {
    console.log(user);
    throw redirect("/login");
  }

  const username = user.username;
  const title = `${username!.at(0).toUpperCase()}` +
    `${username!.slice(1)}'s Cloud Console`;

  let app = appStore.getState();
  if (!app.name) {
    const result = await getApp(user.cookie);
    result.match(
      (app: App) => {
        appStore.getState().updateApp(app);
      },
      (err: ErrorState) => {
        errorStore.getState().setError(err);
      });
    console.log(result);
  }

  let installation = installationStore.getState();
  if (!installation.appSlug) {
    const result = await getInstall(user.cookie);
    result.match(
      (install: Installation) => {
        installationStore.getState().updateInstallation(install);
      },
      (err: ErrorState) => {
        errorStore.getState().setError(err);
      });
    console.log(result);
  }

  return {
    app: app,
    installation: installation,
    title: title,
    footer: 'Just Keep Showing Up & Life Will Reward You',
  };
}

export default function Cloud() {
  let data = useLoaderData();
  const formRef = useRef<HTMLFormElement>(null);
  const appCreate = appStore(
    (state) => state.createApp,
  );
  const installationCreate = installationStore(
    (state) => state.createInstallation,
  );

  const handleCreateApp = async (event: FormEvent<HTMLFormElement>) => {
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

  const handleCreateInstallation = async (event: FormEvent<HTMLFormElement>) => {
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
    const result = await createInstallation(user.cookie, username);
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
              <Form method="post" ref={formRef} onSubmit={async (e) => { await handleCreateApp(e) }}>
                <CreateAppForm />
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
              <Form method="post" ref={formRef} onSubmit={async (e) => { await handleCreateInstallation(e) }}>
                <CreateInstallationForm />
              </Form>
            )}
          </Box>
        </Flex>
      </GridItem>
    </>
  );
}

