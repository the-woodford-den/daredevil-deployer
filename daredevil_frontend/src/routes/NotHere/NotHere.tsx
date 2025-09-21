import { Typography } from '@progress/kendo-react-common';
import { Calendar } from '@progress/kendo-react-dateinputs';
import { GridLayout, GridLayoutItem } from '@progress/kendo-react-layout';
import './NotHere.scss';


function NotHere() {
  return (
    <GridLayout
      align={{ horizontal: 'center', vertical: 'middle' }}
      cols={[{ width: '33.33%' }, { width: '33.34%' }, { width: '33.33%' }]}
      gap={{ rows: 30, cols: 5 }}
    >
      <GridLayoutItem colSpan={3}>
        <Typography.h2>Route Not Found!</Typography.h2>
      </GridLayoutItem>
      <GridLayoutItem colSpan={3}></GridLayoutItem>
      <GridLayoutItem colSpan={3}>
        <Calendar weekNumber showOtherMonthDays />
      </GridLayoutItem>
      <GridLayoutItem colSpan={3}>
        <Typography.h5>Try Again!</Typography.h5>
      </GridLayoutItem>
      <GridLayoutItem colSpan={3}></GridLayoutItem>
    </GridLayout>
  )
}

export default NotHere;
