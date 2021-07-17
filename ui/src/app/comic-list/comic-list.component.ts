import { Component, OnInit } from '@angular/core';
import { ComicService } from '../comic.service';

@Component({
  selector: 'app-comic-list',
  templateUrl: './comic-list.component.html',
  styleUrls: ['./comic-list.component.css']
})
export class ComicListComponent implements OnInit {

  all_comics:any=[];

  constructor(private service:ComicService) { }

  ngOnInit(): void {
    this.service.getAllNames().subscribe(data=>{
      this.all_comics = data;
    })
  }
    
}
