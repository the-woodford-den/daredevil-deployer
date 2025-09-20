import { Typography } from '@progress/kendo-react-common';
import { Calendar } from '@progress/kendo-react-dateinputs';
import { GridLayout, GridLayoutItem } from '@progress/kendo-react-layout';


function NotHere() {
  return (
    <GridLayout
      align={{ horizontal: 'center', vertical: 'middle' }}
      cols={[{ width: '33.33%' }, { width: '33.34%' }, { width: '33.33%' }]}
      rows={[{ height: '20rem' }, { height: '20rem' }]}>
      <GridLayoutItem></GridLayoutItem>
      <GridLayoutItem><Typography.h2>Route Not Found!</Typography.h2></GridLayoutItem>
      <GridLayoutItem></GridLayoutItem>
      <GridLayoutItem></GridLayoutItem>
      <GridLayoutItem>
        <Calendar weekNumber showOtherMonthDays />
      </GridLayoutItem>
      <GridLayoutItem></GridLayoutItem>
      <GridLayoutItem></GridLayoutItem>
      <GridLayoutItem></GridLayoutItem>
      <GridLayoutItem></GridLayoutItem>
    </GridLayout>
  )
}

export default NotHere;
