import * as React from "react";

import {
  Grid,
  GridColumn,
  GridToolbar,
  type GridDetailRowProps,
  type GridDetailExpandChangeEvent,
  type GridGroupExpandChangeEvent,
} from "@progress/kendo-react-grid";
import { type DetailExpandDescriptor, type GroupExpandDescriptor } from "@progress/kendo-react-data-tools";

import data from "./data.json";
import { Button } from "@progress/kendo-react-buttons";
import { AppBar, AppBarSection } from "@progress/kendo-react-layout";

const DetailComponent = (props: GridDetailRowProps) => {
  const dataItem = props.dataItem;

  return (
    <div>
      <section style={{ width: "12rem", float: "left" }}>
        <p>
          <strong>{dataItem}</strong>
        </p>
      </section>
      <Grid style={{ width: "30rem" }} data={dataItem.detail} />
    </div>
  );
};

export default function GridVite() {
  const [groupExpand, setGroupExpand] = React.useState<GroupExpandDescriptor[]>([]);
  const [detailExpand, setDetailExpand] = React.useState<DetailExpandDescriptor>({});

  const handleGroupExpand = (event: GridGroupExpandChangeEvent) => {
    setGroupExpand(event.groupExpand);
  };

  const handleDetailExpandChange = (event: GridDetailExpandChangeEvent) => {
    setDetailExpand(event.detailExpand);
  };

  return (
    <>
      <AppBar position="top">
        <AppBarSection>
          <Button themeColor="primary" fillMode="flat" className="k-mr-1">
            <a href="/">Home</a>
          </Button>
        </AppBarSection>
      </AppBar>
      <div className="k-mt-4">
        <Grid
          id="test"
          style={{ height: "40rem" }}
          sortable={true}
          defaultSort={[{ field: "orderDate", dir: "desc" }]}
          filterable={true}
          groupable={true}
          defaultGroup={[{ field: "githubUsername" }]}
          reorderable={true}
          pageable={{ buttonCount: 4, pageSizes: true }}
          defaultTake={20}
          defaultSkip={0}
          data={data}
          autoProcessData={true}
          dataItemKey="orderID"
          detail={DetailComponent}
          detailExpand={detailExpand}
          onDetailExpandChange={handleDetailExpandChange}
          groupExpand={groupExpand}
          onGroupExpandChange={handleGroupExpand}
        >
          <GridToolbar>
            <Button themeColor="primary" fillMode="flat" className="k-mr-1">README.md</Button>
            &nbsp;
            <Button themeColor="primary" fillMode="flat" className="k-mr-1">DEPLOY</Button>
          </GridToolbar>
          <GridColumn field="githubUsername" width="18rem" />
          <GridColumn field="githubID" width="18rem" />
          <GridColumn field="githubAppName" width="18rem" />
          <GridColumn field="githubAppID" width="18rem" />
        </Grid>
      </div>
    </>
  );
}
