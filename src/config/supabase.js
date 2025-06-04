import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://jsyjrlhilcdgtmavjnvz.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InphdGZiZ3B2bHlsdnNjenR4Y2l3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODQ1NTcyOSwiZXhwIjoyMDY0MDMxNzI5fQ.uS8O66wh1ey3SgGIB683v4b9Q2nZqzeZ9o6OMn266mA'

export const supabase = createClient(supabaseUrl, supabaseKey)