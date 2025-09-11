import { Grid, GridColumn } from '@progress/kendo-react-grid'
import { DropDownList, type DropDownListChangeEvent } from '@progress/kendo-react-dropdowns'
import React from 'react';
import './App.scss';
import products from './products.json'
import categories from './categories.json'

function App() {

  const [category, setCategory] = React.useState(null)

  const handleDropDownChange = React.useCallback((event: DropDownListChangeEvent) => {
    setCategory(event.target.value.CategoryID)
  }, []);

  return (
    <div className="App">
      <h1>Daredevil</h1>
      <Grid data={products}>
        <GridColumn field="ProductName" />
        <GridColumn field="UnitPrice" />
        <GridColumn field="UnitsInStock" />
        <GridColumn field="Discontinued" />
      </Grid>

      <h2>Hello KendoReact!</h2>
      <p>
        <DropDownList
          data={categories}
          dataItemKey="CategoryID"
          textField="CategoryName"
          defaultItem={{ CategoryID: null, CategoryName: 'Product categories' }}
          onChange={handleDropDownChange}
        />
        &nbsp; Selected category ID: <strong>{category}</strong>
      </p>
    </div>
  )
}

export default App

