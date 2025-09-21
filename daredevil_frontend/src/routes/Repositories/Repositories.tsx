import { useState } from "react";

import {
  Grid,
  GridToolbar
} from "@progress/kendo-react-grid";
import { type Repository } from './Repositories.ts';
import { Button } from "@progress/kendo-react-buttons";
import data from "../../assets/data.json";


const repos: Repository[] = data.map((x) => {
  return x as Repository;
})
function Repositories() {
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

export default Repositories;
