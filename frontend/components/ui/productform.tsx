"use client";
import { useState, useEffect } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Card, CardContent } from "./card";
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
import { Input } from "./input";
import { Skeleton } from "./skeleton";

interface Product {
  ProductTitle: string;
  price: number;
  ImageURL: string;
}

const FormSchema = z.object({
  user_id: z.string().min(1, {
    message: "User ID is required.",
  }),
  question: z.string().min(2, {
    message: "Query must be at least 2 characters.",
  }),
});

export function ProductForm() {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      user_id: "",
      question: "",
    },
  });

  async function onSubmit(data: z.infer<typeof FormSchema>) {
    try {
      setIsLoading(true);
      const response = await fetch("/api/v1/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error("Failed to fetch data");

      const result = await response.json();
      const productEntries = result.result
        .split(/^\d+\.\s|\n\d+\.\s/)
        .map((entry: string) => entry.trim())
        .filter(Boolean);

      const parsedProducts = productEntries.map((entry: string): Product => {
        const titleMatch = entry.match(/^(.*?)\n/);
        const priceMatch = entry.match(/Price: \$(\d+\.?\d*)/);
        const imageMatch = entry.match(/\((.*?)\)/);

        return {
          ProductTitle: titleMatch?.[1] || "",
          price: parseFloat(priceMatch?.[1] || "0"),
          ImageURL: imageMatch?.[1] || "",
        };
      });
      // Show success toast
      setProducts(parsedProducts);
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
                  <Input placeholder="1" {...field} />
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
                <FormLabel className="text-white">Enter Query</FormLabel>
                <FormControl>
                  <Input
                    placeholder="recommend me footwears for women"
                    {...field}
                  />
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
      {/* Form code */}
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
        products &&
        products.length > 0 && (
          <Card className="p-4 mt-4 bg-black text-white">
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
                  <h2 className="text-lg font-medium text-center">
                    {product.ProductTitle}
                  </h2>
                  <p className="text-base">Price: ${product.price}</p>
                </div>
              ))}
            </div>
          </Card>
        )
      )}
    </>
  );
}
