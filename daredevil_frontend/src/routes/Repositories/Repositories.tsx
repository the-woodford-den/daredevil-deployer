import { useState } from "react";

import {
  Grid,
  GridToolbar
} from "@progress/kendo-react-grid";
import { Button } from "@progress/kendo-react-buttons";


function Repositories() {
  const [data] = useState([
    { Column1: 'A1', Column2: 'A2' },
    { Column1: 'B1', Column2: 'B2' },
    { Column1: 'C1', Column2: 'C2' }
  ]);

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
