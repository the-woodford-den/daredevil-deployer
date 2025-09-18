export interface ProductCategory {
  Category?: ProductCategory,
  CategoryID?: number,
  CategoryName?: string,
  Description?: string,
  Discontinued?: boolean,
  OrderID?: number,
  ProductID: number,
  ProductName?: string,
  QuantityPerUnit?: string,
  ReorderLevel?: number,
  SupplierID?: number,
  UnitPrice?: number,
  UnitsInStock?: number,
  UnitsOnOrder?: number,
  city: string,
  country: string
  customerID: string,
  details?: any
  discount: number
  employeeID: number,
  expanded?: boolean,
  field?: string,
  filter?: "boolean" | "numeric" | "text" | "date" | undefined,
  firstName: string,
  freight: number,
  id: number,
  inEdit?: boolean | string,
  lastName: string,
  locked?: boolean
  minGridWidth?: number,
  minWidth?: number,
  orderDate?: Date,
  orderID: number,
  postalCode: number,
  productID: number,
  quantity: number,
  region: string,
  requiredDate: Date,
  shipName: string,
  shipVia: number,
  shippedDate?: Date,
  show?: boolean,
  street: string,
  title: string
  unitPrice: number,
  width?: string | number
};

