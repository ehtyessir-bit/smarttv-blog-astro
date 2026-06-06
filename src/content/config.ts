import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title:       z.string(),
    description: z.string(),
    date:        z.string(),
    keywords:    z.string().optional(),
    mainSite:    z.string().optional().default('https://smarttv.one'),
    noindex:     z.boolean().optional().default(false),
    image:       z.string().optional(),
    faq:         z.array(z.object({ q: z.string(), a: z.string() })).optional(),
  }),
});

export const collections = { blog };
