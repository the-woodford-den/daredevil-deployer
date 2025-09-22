import { useState } from 'react';

import { Grid, GridToolbar } from '@progress/kendo-react-grid';
import { type Repository } from './types';
import { Button } from '@progress/kendo-react-buttons';
import data from '~/data.json';
import './style.scss';

const repos: Repository[] = (data as Repository[]).map((x: Repository) => {
  return x;
});
export function Repositories() {
  const [data] = useState(repos);

  const customClick = () => {
    alert('Custom handler in custom toolbar');
  };

  return (
    <Grid data={data}>
      <GridToolbar>
        <Button title="Click" onClick={customClick}>
          Click
        </Button>
      </GridToolbar>
    </Grid>
  );
}
