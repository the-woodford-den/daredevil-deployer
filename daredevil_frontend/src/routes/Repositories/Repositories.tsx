import * as React from "react";

import { Button } from "@progress/kendo-react-buttons";
import { type DetailExpandDescriptor, type GroupExpandDescriptor } from "@progress/kendo-react-data-tools";
import {
  Grid,
  GridColumn,
  GridToolbar,
  type GridDetailRowProps,
  type GridDetailExpandChangeEvent,
  type GridGroupExpandChangeEvent,
} from "@progress/kendo-react-grid";

import data from "../../assets/data.json";

const DetailComponent = (props: GridDetailRowProps) => {
  const dataItem = props.dataItem;

  return (
    <div>
      <section>
        <p>
          <strong>{dataItem.full_name}</strong>
        </p>
        <p>
          <strong>{dataItem.private}</strong>
        </p>
        <p>
          <strong>{dataItem.description}</strong>
        </p>
        <p>
          <strong>{dataItem.url}</strong>
        </p>
        <p>
          <strong>{dataItem.language}</strong>
        </p>
        <p>
          <strong>{dataItem.default_branch}</strong>
        </p>
        <p>
          <strong>{dataItem.visibility}</strong>
        </p>
        <p>
          <strong>{dataItem.pushed_at}</strong>
        </p>
      </section>
      <Grid data={dataItem.details} />
    </div>
  );
};

function Repositories() {
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
      <div className="k-mt-4">
        <Grid
          id="test"
          sortable={true}
          defaultSort={[{ field: "orderDate", dir: "desc" }]}
          filterable={true}
          groupable={true}
          defaultGroup={[{ field: "full_name" }]}
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
          <GridColumn field="full_name" width="6rem" />
          <GridColumn field="private" width="6rem" />
          <GridColumn field="description" width="6rem" />
          <GridColumn field="url" width="6rem" />
          <GridColumn field="language" width="6rem" />
          <GridColumn field="default_branch" width="6rem" />
          <GridColumn field="visibility" width="6rem" />
          <GridColumn field="pushed_at" width="6rem" />
        </Grid>
      </div>
    </>
  );
}

export default Repositories;
