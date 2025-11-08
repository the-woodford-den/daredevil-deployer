import { Image, Grid, GridItem, Text, Stack, Heading, Highlight, } from '@chakra-ui/react';
import { RegisterForm } from '@/components';
import { userStore } from '@/state';
import rubyUrl from '~/ruby.svg';
import devilUrl from '~/ddevil-pixel.png';
import underUrl from '~/underline.svg';
import type { FormEvent } from 'react';


export default function Register() {

  const createUser = userStore(
    (state) => state.createUser,
  );

  const handleCreateUser = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const name = formData.get("username") as string;
    const email = formData.get("email") as string;
    const pword = formData.get("password") as string;

    const res = await createUser(pword, email, name);
    console.log(res);
  };

  return (
    <Grid
      templateColumns="repeat(4,1fr)"
      width="vw"
      height="vh"
      gap="10"
      alignItems="center"
      justifyItems="center"
    >
      <GridItem colSpan={3}>
        <Image
          src={rubyUrl}
          alt="Ruby"
          boxSize="6rem"
          fit="contain"
          className="rubyLogo"
        />
      </GridItem>
      <GridItem
        colSpan={3}
        alignItems="center"
        justifyItems="center"
      >
        <Text>
          The Woodford Den: Daredevil Deployer Registration
        </Text>
      </GridItem>
      <GridItem colSpan={3} alignItems="center" justifyItems="center">
        <Heading size="xl" mb="5" className="t-font">
          Cloud Console
        </Heading>
      </GridItem>
      <GridItem colSpan={3} alignItems="center" justifyItems="center">
        <Image
          transitionProperty="position"
          transitionBehavior="slide-fade-in"
          animation="spin"
          animationTimeline="auto"
          src={devilUrl}
        />
      </GridItem>
      <GridItem colSpan={3} alignItems="center" justifyItems="center">
        <Image
          maxWidth="50%"
          animation="spin"
          src={rubyUrl}
        />
      </GridItem>
      <GridItem colSpan={3} alignItems="center" justifyItems="center">
        <Stack>
          <Heading size="2xl" letterSpacing="wider">
            <Highlight query="Life Will Reward" styles={{ color: "teal.600", }}>
              Life Will Reward The Brave
            </Highlight>
          </Heading>
          <Image
            brightness="100"
            captionSide="MEGAMAN!"
            src={underUrl}
            alt="line"
          />
        </Stack>
      </GridItem>
      <GridItem
        colSpan={3}
        bgColor="honeydew"
        alignItems="center"
        justifyItems="center"
        animationStyle="slide-fade-in"
      >
        <form onSubmit={handleCreateUser}>
          <RegisterForm />
        </form>
      </GridItem>
    </Grid >
  );
};

