import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ComicService } from 'src/app/comic.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {

  constructor(private service:ComicService, private router:Router) {     
  }

  ngOnInit(): void {
  }

}
