package com.linuxproject

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.util.concurrent.TimeUnit

class MainActivity : AppCompatActivity() {
    
    private lateinit var recyclerView: RecyclerView
    private lateinit var swipeRefresh: SwipeRefreshLayout
    private lateinit var adapter: ItemsAdapter
    private val items = mutableListOf<DisplayItem>()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        recyclerView = findViewById(R.id.recyclerView)
        swipeRefresh = findViewById(R.id.swipeRefresh)
        
        recyclerView.layoutManager = LinearLayoutManager(this)
        adapter = ItemsAdapter(items)
        recyclerView.adapter = adapter
        
        swipeRefresh.setOnRefreshListener {
            fetchData()
        }
        
        fetchData()
    }
    
    private fun fetchData() {
        swipeRefresh.isRefreshing = true
        
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val url = "https://raw.githubusercontent.com/flanux/linux-project-mobile/main/scrapers/output/data.json"
                
                val client = OkHttpClient.Builder()
                    .connectTimeout(30, TimeUnit.SECONDS)
                    .readTimeout(30, TimeUnit.SECONDS)
                    .build()
                
                val request = Request.Builder().url(url).build()
                val response = client.newCall(request).execute()
                
                if (response.isSuccessful) {
                    val jsonString = response.body?.string() ?: "{}"
                    val json = JSONObject(jsonString)
                    
                    val newItems = mutableListOf<DisplayItem>()
                    
                    // Parse internships
                    if (json.has("internships")) {
                        val internshipsArray = json.getJSONArray("internships")
                        if (internshipsArray.length() > 0) {
                            newItems.add(DisplayItem.Header("Internships & Mentorship"))
                            for (i in 0 until internshipsArray.length()) {
                                val obj = internshipsArray.getJSONObject(i)
                                newItems.add(DisplayItem.Internship(
                                    title = obj.optString("title", ""),
                                    organization = obj.optString("organization", ""),
                                    description = obj.optString("description", ""),
                                    link = obj.optString("link", "")
                                ))
                            }
                        }
                    }
                    
                    // Parse jobs
                    if (json.has("jobs")) {
                        val jobsArray = json.getJSONArray("jobs")
                        if (jobsArray.length() > 0) {
                            newItems.add(DisplayItem.Header("Jobs"))
                            for (i in 0 until jobsArray.length()) {
                                val obj = jobsArray.getJSONObject(i)
                                newItems.add(DisplayItem.Job(
                                    title = obj.optString("title", ""),
                                    company = obj.optString("company", ""),
                                    location = obj.optString("location", ""),
                                    link = obj.optString("link", "")
                                ))
                            }
                        }
                    }
                    
                    // Parse news
                    if (json.has("news")) {
                        val newsArray = json.getJSONArray("news")
                        if (newsArray.length() > 0) {
                            newItems.add(DisplayItem.Header("Latest News"))
                            for (i in 0 until newsArray.length()) {
                                val obj = newsArray.getJSONObject(i)
                                newItems.add(DisplayItem.News(
                                    title = obj.optString("title", ""),
                                    source = obj.optString("source", ""),
                                    link = obj.optString("link", ""),
                                    date = obj.optString("date", "")
                                ))
                            }
                        }
                    }
                    
                    // Parse projects
                    if (json.has("projects")) {
                        val projectsArray = json.getJSONArray("projects")
                        if (projectsArray.length() > 0) {
                            newItems.add(DisplayItem.Header("Projects"))
                            for (i in 0 until projectsArray.length()) {
                                val obj = projectsArray.getJSONObject(i)
                                newItems.add(DisplayItem.Project(
                                    name = obj.optString("name", ""),
                                    description = obj.optString("description", ""),
                                    category = obj.optString("category", ""),
                                    link = obj.optString("link", "")
                                ))
                            }
                        }
                    }
                    
                    // Parse learning resources
                    if (json.has("learning")) {
                        val learningArray = json.getJSONArray("learning")
                        if (learningArray.length() > 0) {
                            newItems.add(DisplayItem.Header("Learning Resources"))
                            for (i in 0 until learningArray.length()) {
                                val obj = learningArray.getJSONObject(i)
                                newItems.add(DisplayItem.Learning(
                                    title = obj.optString("title", ""),
                                    type = obj.optString("type", ""),
                                    source = obj.optString("source", ""),
                                    link = obj.optString("link", "")
                                ))
                            }
                        }
                    }
                    
                    withContext(Dispatchers.Main) {
                        items.clear()
                        items.addAll(newItems)
                        adapter.notifyDataSetChanged()
                        swipeRefresh.isRefreshing = false
                        
                        if (items.isEmpty()) {
                            Toast.makeText(
                                this@MainActivity,
                                "No data available. Pull to refresh.",
                                Toast.LENGTH_LONG
                            ).show()
                        }
                    }
                } else {
                    withContext(Dispatchers.Main) {
                        swipeRefresh.isRefreshing = false
                        Toast.makeText(
                            this@MainActivity,
                            "Failed to fetch data: ${response.code}",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
                withContext(Dispatchers.Main) {
                    swipeRefresh.isRefreshing = false
                    Toast.makeText(
                        this@MainActivity,
                        "Error: ${e.message}",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        }
    }
}

sealed class DisplayItem {
    data class Header(val title: String) : DisplayItem()
    data class Internship(
        val title: String,
        val organization: String,
        val description: String,
        val link: String
    ) : DisplayItem()
    data class Job(
        val title: String,
        val company: String,
        val location: String,
        val link: String
    ) : DisplayItem()
    data class News(
        val title: String,
        val source: String,
        val link: String,
        val date: String
    ) : DisplayItem()
    data class Project(
        val name: String,
        val description: String,
        val category: String,
        val link: String
    ) : DisplayItem()
    data class Learning(
        val title: String,
        val type: String,
        val source: String,
        val link: String
    ) : DisplayItem()
}
