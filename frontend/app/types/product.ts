export interface Product {
    ProductId: number;
    ProductTitle: string;
    ImageURL: string;
    price: number;
  }
  
  export interface ApiResponse {
    message: string;
    query_rows: Product[];
  }