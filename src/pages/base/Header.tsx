import { Box, Container, Group, Text, Tooltip } from '@mantine/core';
import { IconBrandGithub, IconEye, IconHome } from '@tabler/icons-react';
import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useStore } from '../../store.ts';
import classes from './Header.module.css';

export function Header(): ReactNode {
  const location = useLocation();
  const algorithm = useStore(state => state.algorithm);

  const links = [
    <Link
      key="home"
      to={`/${location.search}`}
      className={classes.link}
      data-active={location.pathname === '/' || undefined}
    >
      <Box hiddenFrom="xs">
        <IconHome size={18} />
      </Box>
      <Box visibleFrom="xs">Home</Box>
    </Link>,
  ];

  if (algorithm !== null) {
    links.push(
      <Link
        key="visualizer"
        to={`/visualizer${location.search}`}
        className={classes.link}
        data-active={location.pathname === '/visualizer' || undefined}
      >
        <Box hiddenFrom="xs">
          <IconHome size={18} />
        </Box>
        <Box visibleFrom="xs">Visualizer</Box>
      </Link>,
    );
  } else {
    links.push(
      <Tooltip key="visualizer" label="Load an algorithm first">
        <a className={`${classes.link} ${classes.linkDisabled}`}>
          <Box hiddenFrom="xs">
            <IconEye size={18} />
          </Box>
          <Box visibleFrom="xs">Visualizer</Box>
        </a>
      </Tooltip>,
    );
  }

  return (
    <header className={classes.header}>
      <Container size="md" className={classes.inner}>
        <Text size="xl" fw={700}>
          <IconEye size={30} className={classes.icon} />
          IMC Prosperity 4 Visualizer
        </Text>

        <Group gap={5}>
          {links}
          <Tooltip label="rkothari3 — this fork" position="bottom">
            <a
              href="https://github.com/rkothari3"
              target="_blank"
              rel="noreferrer"
              className={classes.link}
              aria-label="rkothari3 on GitHub"
            >
              <IconBrandGithub size={18} />
            </a>
          </Tooltip>
          <Tooltip label="jmerle — original creator" position="bottom">
            <a
              href="https://github.com/jmerle"
              target="_blank"
              rel="noreferrer"
              className={classes.link}
              aria-label="jmerle on GitHub"
            >
              <IconBrandGithub size={18} style={{ opacity: 0.55 }} />
            </a>
          </Tooltip>
        </Group>
      </Container>
    </header>
  );
}
