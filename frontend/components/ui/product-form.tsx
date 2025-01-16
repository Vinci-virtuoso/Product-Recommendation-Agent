"use client";
import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Card } from "./card";
import { toast } from "../hooks/use-toast";
import { Button } from "./button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "./form";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "./select";
import { Input } from "./input";
import { Skeleton } from "./skeleton";

interface Product {
  ProductTitle: string;
  price: number;
  ImageURL: string;
  Date?: string;
  Time?: string;
  total_amount: number;
}

const FormSchema = z.object({
  user_id: z.string().min(1, {
    message: "User ID is required.",
  }),
  question: z.string().min(1, {
    message: "Please select a query type.",
  }),
  user_input: z.string().optional(),
});

export function ProductForm() {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const [isRecommendationQuery, setIsRecommendationQuery] = useState(false);
  const [isOrderQuery, setIsOrderQuery] = useState(false);
  const [isOrderHistoryQuery, setIsOrderHistoryQuery] = useState(false);
  const [orderData, setOrderData] = useState<string>("");

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      user_id: "",
      question: "",
    },
  });

  const handleQueryType = (question: string) => {
    setIsRecommendationQuery(question === "RecommendationQuery");
    setIsOrderQuery(question === "OrderQuery");
    setIsOrderHistoryQuery(question === "OrderHistoryQuery");
  };

  async function onSubmit(data: z.infer<typeof FormSchema>) {
    try {
      setIsLoading(true);
      handleQueryType(data.question);
      const combinedQuestion = data.user_input
      ? `${data.question}: ${data.user_input}`
      : data.question;
    const response = await fetch("/api/v1/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: data.user_id,
        question: combinedQuestion,
      }),
    });

      if (!response.ok) throw new Error("Failed to fetch data");

      const result = await response.json();

      if (data.question === "RecommendationQuery") {
        const productEntries = result.result
        .split(/(?=^\d+\.|\n\d+\.)/m)
        .map((entry: string) => entry.trim())
        .filter((entry: string) => entry && entry.length > 0 && /\d+\./.test(entry));

        const parsedProducts = productEntries.map((entry: string): Product => {
          const titleMatch = entry.match(/^(.*?)\n/);
          const priceMatch = entry.match(/Price: \$(\d+\.?\d*)/);
          const imageMatch = entry.match(/\((https?:\/\/[^\s)]+)\)/);
          const totalAmountMatch = entry.match(/Total amount: \$(\d+\.\d{2})/);

          return {
            ProductTitle: titleMatch?.[1]?.trim() || "",
            price: parseFloat(priceMatch?.[1] || "0"),
            ImageURL: imageMatch?.[1] || "",
            total_amount: totalAmountMatch ? parseFloat(totalAmountMatch[1]) : 0,
          };
        });
        setProducts(parsedProducts);
      } else if (data.question === "OrderHistoryQuery") {
        const orderEntries = result.result
        .split(/(?=^\d+\.|\n\d+\.)/m)
        .map((entry: string) => entry.trim())
        .filter((entry: string) => entry && entry.length > 0 && /\d+\./.test(entry));

        const parsedOrders = orderEntries.map((entry: string) => {
          const dateTimeMatch = entry.match(
            /Order placed on (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})/
          );
          const totalAmountMatch = entry.match(/Total amount: \$(\d+\.\d{2})/);
          const priceMatch = entry.match(/Price: \$(\d+\.\d{2})/);
          
          
          
          
          return {
            Date: dateTimeMatch?.[1] || "",
            Time: "",
            price: parseFloat(priceMatch?.[1] || "0"),
            total_amount: totalAmountMatch ? parseFloat(totalAmountMatch[1]) : 0,
            ImageURL: "",
            ProductTitle: "",
            
          };
        });
        setProducts(parsedOrders);
      } else if (data.question === "OrderQuery") {
        setOrderData(result.result);
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to process query",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <>
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="w-full space-y-4"
        >
          <FormField
            control={form.control}
            name="user_id"
            render={({ field }) => (
              <FormItem>
                <FormLabel className="text-white">User ID</FormLabel>
                <FormControl>
                  <Input placeholder="" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="question"
            render={({ field }) => (
              <FormItem>
                <FormLabel className="text-white">Select Query Type</FormLabel>
                <FormControl>
                  <Select
                    onValueChange={(value) => field.onChange(value)}
                    value={field.value}
                  >
                  <FormField
                      control={form.control}
                      name="user_input"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-white">Your Query</FormLabel>
                          <FormControl>
                            <Input placeholder="Enter your query" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                      />
                    <SelectTrigger>
                      <SelectValue placeholder="Select Query Type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="RecommendationQuery">
                        Recommendation Query
                      </SelectItem>
                      <SelectItem value="OrderQuery">Order Query</SelectItem>
                      <SelectItem value="OrderHistoryQuery">
                        Order History Query
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button
            type="submit"
            className="w-24 bg-white text-black rounded-md"
            disabled={isLoading}
          >
            {isLoading ? "Loading..." : "Submit"}
          </Button>
        </form>
      </Form>
      {/* Display components */}
      {isLoading ? (
        <Card className="p-4 mt-4 bg-black text-white">
          <div className="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-4">
            {Array.from({ length: 5 }).map((_, index) => (
              <div
                key={index}
                className="flex flex-col items-center space-y-4"
              >
                <Skeleton className="w-full h-[260px] rounded-md" />
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-4 w-1/2" />
              </div>
            ))}
          </div>
        </Card>
      ) : (
        <>
         {isRecommendationQuery && products && products.length > 0 && (
          <Card className="p-4 mt-4 bg-black text-white">
            <div className="font-mono">
              <div className="text-lg mb-2">Results:</div>
              <div className="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-4">
                {products.map((product, index) => (
                  <div
                    key={index}
                    className="flex flex-col items-center space-y-4"
                  >
                    <img
                      src={product.ImageURL}
                      alt={product.ProductTitle}
                      className="w-full h-[260px] object-cover rounded-md"
                    />
                    <div className="w-3/4 text-center">
                      <h2 className="text-lg font-medium">
                        {product.ProductTitle}
                      </h2>
                    </div>
                    <div className="w-1/2 text-center">
                      <p className="text-base">Price: ${product.price}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        )}
    {isOrderHistoryQuery && products && products.length > 0 && (
      <Card className="p-4 mt-4 bg-black text-white">
        <div className="font-mono">
          <div className="text-lg mb-2">Results:</div>
          <div className="grid grid-cols-1 gap-4">
            {products.map((order, index) => (
              <div 
                key={index}
                className="flex items-center justify-between p-3 border border-gray-800 rounded-md"
              >
                <div className="flex flex-col">
                  <div className="text-base">
                    {order.Date} {order.Time}
                  </div>
                  <div className="text-base text-gray-400">
                    Order #{index + 1}
                  </div>
                </div>
                <div className="text-base font-medium">
                  Total Amount: ${order.total_amount.toFixed(2)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </Card>
      )}
          {isOrderQuery && orderData && (
            <Card className="p-4 mt-4 bg-black text-white">
              <div className="font-mono">
                <div className="text-lg mb-2">Results:</div>
                <div>
                  {orderData}
                </div>
              </div>
            </Card>
          )}
        </>
      )}
    </>
  );
}
